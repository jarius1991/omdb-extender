from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core import models


class FavouriteMovieSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.FavouriteMovie
        fields = ['id', 'user', 'movie_id']
        validators = [
            UniqueTogetherValidator(
                queryset=models.FavouriteMovie.objects.all(),
                fields=['user', 'movie_id']
            )
        ]


class MovieToWatchSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.MovieToWatch
        fields = ['id', 'user', 'movie_id']
        validators = [
            UniqueTogetherValidator(
                queryset=models.MovieToWatch.objects.all(),
                fields=['user', 'movie_id']
            )
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Review
        fields = ['id', 'user', 'movie_id', 'rating', 'review']
        validators = [
            UniqueTogetherValidator(
                queryset=models.Review.objects.all(),
                fields=['user', 'movie_id']
            )
        ]
