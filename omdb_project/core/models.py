from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


class MovieToWatch(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='movies_to_watch', on_delete=models.CASCADE)
    movie_id = models.CharField(max_length=400)

    class Meta:
        unique_together = ['user', 'movie_id']

    def __str__(self):
        return f'{self.user.username} want to watch {self.movie_id}'


class FavouriteMovie(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='favourite_movies', on_delete=models.CASCADE)
    movie_id = models.CharField(max_length=400)

    class Meta:
        unique_together = ['user', 'movie_id']

    def __str__(self):
        return f'{self.user.username} really likes {self.movie_id}'


class Review(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='reviewed_movies', on_delete=models.CASCADE)
    movie_id = models.CharField(max_length=400)
    rating = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    review = models.TextField(blank=True, max_length=2000)

    class Meta:
        unique_together = ['user', 'movie_id']

    def __str__(self):
        return f'{self.user.username} rates {self.movie_id} {self.rating} and think: {self.review}'
