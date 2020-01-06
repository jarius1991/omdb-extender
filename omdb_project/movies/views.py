import asyncio
import aiohttp
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from core import models
from movies import serializers
from movies import permissions

from core.omdb import Omdb_API


class BaseListMovieViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    """The view with predefined features for movies list endpoints"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, permissions.IsUserOrReadOnly)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('movie_id')


class FavouriteMovieViewSet(BaseListMovieViewSet):
    """The view for favourite movie model"""
    queryset = models.FavouriteMovie.objects.all()
    serializer_class = serializers.FavouriteMovieSerializer


class MovieToWatchViewSet(BaseListMovieViewSet):
    """The view for movie to watch model"""
    queryset = models.MovieToWatch.objects.all()
    serializer_class = serializers.MovieToWatchSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """The view for review model"""
    serializer_class = serializers.ReviewSerializer
    queryset = models.Review.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, permissions.IsUserOrReadOnly)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'movie_id']

    def perform_create(self, serializer):
        """Ensure that saved user is authenticated user"""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Ensure that saved user is authenticated user"""
        serializer.save(user=self.request.user)


class MovieViewSet(viewsets.ViewSet):
    """
    View to display a list of movies from omdb. Provides the option of filtering the title and genre.
    Title is required.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        title = request.query_params.get('title')
        genre = request.query_params.get('genre')
        page = request.query_params.get('page', 1)
        if not title:
            return Response("'title' parameter is required", status=status.HTTP_400_BAD_REQUEST)
        try:
            movies = cache.get(f'movie_{title}')
            # Get movies if they are not in cache
            if not movies:
                movies = asyncio.run(self._get_movies(title=title))
                cache.set(f'movie_{title}', movies, 60*60*2)
            # Filter movies if the user has specified a genre
            if genre:
                movies = Omdb_API.filter_movies_by_genre(movies=movies, genre=genre)
        except Exception as e:
            return Response(f'OMDB API does not work correctly. Original message: {e}',
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(self._get_page(movies, page))

    async def _get_movies(self, title):
        async with aiohttp.ClientSession() as session:
            return await Omdb_API(session).search_movies(title=title)

    def _get_page(self, movies, page, page_size=10):
        paginator = Paginator(movies, page_size)
        try:
            movie_page = paginator.page(page)
        except PageNotAnInteger:
            movie_page = paginator.page(1)
        except EmptyPage:
            movie_page = paginator.page(paginator.num_pages)
        return list(movie_page)
