from functools import partial

from django.core.cache import cache

from django_filters.rest_framework import DjangoFilterBackend
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
    View to display a list of movies from omdb. Provides the option of filtering the title and genre. Title is required.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        api = Omdb_API()
        title = request.query_params.get('title')
        genre = request.query_params.get('genre')
        if not title:
            return Response("'title' parameter is required", status=status.HTTP_400_BAD_REQUEST)
        try:
            movie_list = cache.get_or_set(f'{title},{genre}',
                                          partial(api.search_movies, title=title, genre=genre),
                                          timeout=60 * 60)
        except Exception as e:
            return Response(f'OMDB API does not work correctly. Original message: {e}',
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(movie_list)
