import asyncio
from asyncio import create_task
from urllib import parse  # , request
from functools import partial
import json

import aiohttp

from django.conf import settings
from django.core.cache import cache


class Omdb_API:
    OMDB_URL = "http://www.omdbapi.com/?"
    OMDB_API_KEY = settings.OMDB_API_KEY

    def __init__(self):
        self.session = aiohttp.ClientSession()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def search_movies(self, title, genre=None):
        """
        :param title: Movie title to search for.
        :param genre: The genre of movies that should be returned.
        :return: List of searched movies
        """
        def _async_loop():
            return asyncio.run(self._get_movie_list_with_genre(title=title))

        movies = cache.get_or_set(f'{title}',
                                  _async_loop,
                                  timeout=60 * 60)
        if genre:
            movies = self._filter_movies_by_genre(movies, genre)
        return movies

    def close(self):
        """Method to close session"""
        await self.session.close()

    async def _get_movie_list_with_genre(self, title):
        movie_list = self._get_movie_list(title=title)
        self._add_genre_data_to_movies(movies=movie_list)
        return movie_list

    def _get_movie_list(self, title):
        """Return movie list with short description"""
        params = {'s': title, 'apikey': self.OMDB_API_KEY}
        movies = []

        response = await self._run_query(**params)
        movies.extend(response['Search'])
        rest_page_numbers = range(2, self._page_count(response) + 1)

        movie_page_tasks = [create_task(self._run_query(page=page, **params)) for page in rest_page_numbers]
        if movie_page_tasks:
            rest_movie_pages = await asyncio.gather(movie_page_tasks)
            for movie_page in rest_movie_pages:
                movies.extend(movie_page['Search'])
        return movies

    def _add_genre_data_to_movies(self, movies):
        add_genre_tasks = [create_task(self._add_movie_genre(movie)) for movie in movies]
        await asyncio.gather(add_genre_tasks)

    async def _add_movie_genre(self, movie):
        params = {'i': movie["imdbID"], 'apikey': self.OMDB_API_KEY}
        movie_data = await self._run_query(**params)
        movie['Genre'] = movie_data['Genre'].split(', ')

    def _filter_movies_by_genre(self, movies, genre):
        """Return videos that match genre"""
        return list(filter(lambda movie: genre in movie['Genre'], movies))

    async def _run_query(self, **params):
        """Return response for requested parameters"""
        async with self.session.get(self.OMDB_URL, params=params) as resp:
            return await resp.json()
        # querystring = parse.urlencode(params)
        # url = self.OMDB_URL + querystring
        # resp = request.urlopen(url)
        #
        # return json.loads(resp.read())

    def _page_count(self, response):
        """Return numbers of pages for requested search"""
        total_results = int(response['totalResults'])
        full_pages, remainder = divmod(total_results, 10)
        return full_pages + 1 if remainder else full_pages
