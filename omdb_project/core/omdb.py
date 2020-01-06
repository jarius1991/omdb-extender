import asyncio
from asyncio import create_task

from django.conf import settings

from .exceptions import SessionRequiredException


class Omdb_API:
    OMDB_URL = "http://www.omdbapi.com/?"
    OMDB_API_KEY = settings.OMDB_API_KEY

    def __init__(self, session=None):
        if session is None:
            raise SessionRequiredException("The session instance must be passed during class initialization!")
        self.session = session

    async def search_movies(self, title):
        """
        :param title: Movie title to search for.
        :return: List of searched movies
        """
        movies = await self._get_movie_list(title=title)
        await self._add_genre_data_to_movies(movies=movies)
        return movies

    @staticmethod
    def filter_movies_by_genre(movies, genre):
        """Return movies that match genre"""
        return list(filter(lambda movie: genre in movie['Genre'], movies))

    async def _get_movie_list(self, title):
        """Return movie list with short description"""
        params = {'s': title, 'apikey': self.OMDB_API_KEY}
        movies = []

        response = await self._run_query(**params)
        movies.extend(response['Search'])
        rest_page_numbers = range(2, self._page_count(response) + 1)

        movie_page_tasks = [create_task(self._run_query(page=page, **params)) for page in rest_page_numbers]
        if movie_page_tasks:
            rest_movie_pages = await asyncio.gather(*movie_page_tasks)
            for movie_page in rest_movie_pages:
                movies.extend(movie_page['Search'])
        return movies

    async def _add_genre_data_to_movies(self, movies):
        add_genre_tasks = [create_task(self._add_movie_genre(movie)) for movie in movies]
        await asyncio.gather(*add_genre_tasks)

    async def _add_movie_genre(self, movie):
        params = {'i': movie["imdbID"], 'apikey': self.OMDB_API_KEY}
        movie_data = await self._run_query(**params)
        movie['Genre'] = movie_data['Genre'].split(', ')

    async def _run_query(self, **params):
        """Return response for requested parameters"""
        async with self.session.get(self.OMDB_URL, params=params) as resp:
            return await resp.json()

    def _page_count(self, response):
        """Return numbers of pages for requested search"""
        total_results = int(response['totalResults'])
        full_pages, remainder = divmod(total_results, 10)
        return full_pages + 1 if remainder else full_pages
