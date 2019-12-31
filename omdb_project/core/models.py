from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


class Movie(models.Model):
    title = models.CharField(max_length=255)
    omdb_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'Title:{self.title}, OmdbID:{self.omdb_id}'


class MovieToWatch(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='movies_to_watch', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'movie']

    def __str__(self):
        return f'{self.user.username} want to watch {self.movie.title}'


class FavouriteMovie(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='favourite_movies', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'movie']

    def __str__(self):
        return f'{self.user.username} really likes {self.movie.title}'

class Review(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='reviewed_movies', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
    review = models.TextField(blank=True, max_length=2000)

    class Meta:
        unique_together = ['user', 'movie']

    def __str__(self):
        return f'{self.user.username} rates {self.movie.title} {self.rating} and think: {self.review}'
