from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from core import models


class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = get_user_model().objects.create(username='Zenek', password='martyniuk')
        cls.user_2 = get_user_model().objects.create(username='Krzysztof', password='krawczyk')

    def test_movies_to_watch_to_str(self):
        """Test MovieToWatch string representation"""
        movie_to_watch = models.MovieToWatch.objects.create(user=self.user_1, movie_id='Id_King_Kong')

        self.assertEqual(str(movie_to_watch), "Zenek want to watch Id_King_Kong")
        self.assertTrue(movie_to_watch.id)

    def test_movies_to_watch_unique(self):
        """Exist only one record containing the same user and movie"""
        models.MovieToWatch.objects.create(user=self.user_1, movie_id='Id_King_Kong')
        models.MovieToWatch.objects.create(user=self.user_2, movie_id='Id_King_Kong')

        self.assertEqual(models.MovieToWatch.objects.all().count(), 2)
        self.assertRaises(IntegrityError, models.MovieToWatch.objects.create,
                          user=self.user_1, movie_id='Id_King_Kong')

    def test_favourite_movie_to_watch_to_str(self):
        """Test FavouriteMovie string representation"""
        favourite_movie = models.FavouriteMovie.objects.create(user=self.user_2, movie_id='Id_Pink_Panther')

        self.assertEqual(str(favourite_movie), 'Krzysztof really likes Id_Pink_Panther')
        self.assertTrue(favourite_movie.id)

    def test_favourite_movie_unique(self):
        """Exist only one record containing the same user and movie"""
        models.FavouriteMovie.objects.create(user=self.user_1, movie_id='Id_Pink_Panther')
        models.FavouriteMovie.objects.create(user=self.user_2, movie_id='Id_Pink_Panther')

        self.assertEqual(models.FavouriteMovie.objects.all().count(), 2)
        self.assertRaises(IntegrityError, models.FavouriteMovie.objects.create,
                          user=self.user_1, movie_id='Id_Pink_Panther')

    def test_review_to_str(self):
        """Test Review string representation"""
        review = models.Review.objects.create(user=self.user_1, movie_id='Id_Pink_Panther',
                                              rating=5, review="This is nice movie!!!")

        self.assertEqual(str(review), "Zenek rates Id_Pink_Panther 5 and think: This is nice movie!!!")
        self.assertTrue(review.id)

    def test_review_review_blank(self):
        """Review field can be blank"""
        review = models.Review.objects.create(user=self.user_1, movie_id='Id_Pink_Panther', rating=5)

        self.assertTrue(review.id)

    def test_movie_rating_unvalid_values(self):
        """Check Reviev rating can have between 1 and 10"""
        unvalid_rating_values = [-10, 0, 11, 100]

        for rating in unvalid_rating_values:
            review = models.Review(user=self.user_1, movie_id='Id_Movie',
                                   rating=rating, review="This is nice movie!!!")
            self.assertRaises(ValidationError, review.full_clean)

    def test_movie_rating_valid_values(self):
        """Check Reviev rating can have between 1 and 10"""
        unvalid_rating_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        for rating in unvalid_rating_values:
            review = models.Review(user=self.user_1, movie_id='Id_Movie',
                                   rating=rating, review="This is nice movie!!!")
            review.full_clean()
