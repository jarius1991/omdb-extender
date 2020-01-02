from urllib import parse, request
import json

from django.conf import settings


class Omdb_API:
    OMDB_URL = "http://www.omdbapi.com/?"
    # OMDB_API_KEY = settings.OMDB_API_KEY
    OMDB_API_KEY = 'daa2c3c6'

    def search_movies(self, title, genre=None):
        """
        :param title: Movie title to search for.
        :param genre: The genre of movies that should be returned.
        :return: List of searched movies
        """
        # TODO async page request
        # TODO async genre filtering
        movies = self._get_movies_list(title)
        self._add_genre_data_to_movies(movies)
        if genre:
            filtered_movies = self._filter_movies_by_genre(movies, genre)
            return filtered_movies
        else:
            return movies

    def _get_movies_list(self, title):
        """Return movies list with short description"""
        params = {'s': title, 'apikey': self.OMDB_API_KEY}
        movies = []

        response = self._run_query(params)
        movies.extend(response['Search'])
        rest_page_numbers = range(2, self._page_count(response) + 1)

        for page in rest_page_numbers:
            params['page'] = page
            movies.extend(self._run_query(params)['Search'])
        return movies

    def _get_movie_genre(self, imdb_id):
        params = {'i': imdb_id, 'apikey': self.OMDB_API_KEY}
        movie_data = self._run_query(params)
        return movie_data['Genre'].split(', ')

    def _add_genre_data_to_movies(self, movies):
        for movie in movies:
            movie['Genre'] = self._get_movie_genre(movie["imdbID"])

    def _filter_movies_by_genre(self, movies, genre):
        """Return videos that match genre"""
        return list(filter(lambda movie: genre in movie['Genre'], movies))

    def _run_query(self, params):
        """Return response for requested parameters"""
        querystring = parse.urlencode(params)
        url = self.OMDB_URL + querystring
        resp = request.urlopen(url)
        return json.loads(resp.read())

    def _page_count(self, response):
        """Return numbers of pages for requested search"""
        total_results = int(response['totalResults'])
        full_pages, remainder = divmod(total_results, 10)
        return full_pages + 1 if remainder else full_pages
