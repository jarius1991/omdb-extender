from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from core.models import FavouriteMovie, MovieToWatch, Review


class TestFavouriteMovieViewSetAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = get_user_model().objects.create(username='user1', password='password_1')
        cls.user_2 = get_user_model().objects.create(username='user2', password='password_2')

    def test_user_can_add_movie_to_favourite(self):
        payload = {
            'movie_id': 'tt123456789'
        }
        url = reverse('movie:favouritemovie-list')
        self.client.force_authenticate(self.user_1)

        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(payload['movie_id'], FavouriteMovie.objects.get(pk=response.data['id']).movie_id)

    def test_user_cant_add_one_movie_twice(self):
        payload = {
            'movie_id': 'tt123456789'
        }
        url = reverse('movie:favouritemovie-list')
        self.client.force_authenticate(self.user_1)

        self.client.post(url, payload)
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_user_who_create_favourite_movie_can_delete_it(self):
        fav_movie_1 = FavouriteMovie.objects.create(user=self.user_1, movie_id='Id_1')
        FavouriteMovie.objects.create(user=self.user_2, movie_id='Id_2')
        fav_movie_1_url = reverse('movie:favouritemovie-detail', kwargs={'pk': fav_movie_1.pk})
        self.client.force_authenticate(self.user_2)

        response = self.client.delete(fav_movie_1_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_field_is_not_taken_from_request(self):
        payload = {
            'movie_id': 'tt123456789',
            'user': self.user_2.pk,
        }
        url = reverse('movie:favouritemovie-list')
        self.client.force_authenticate(self.user_1)

        response = self.client.post(url, payload)

        self.assertEqual(FavouriteMovie.objects.get(id=response.data['id']).user, self.user_1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_show_only_logged_in_user_favourite_movie(self):
        fav_movie_1 = FavouriteMovie.objects.create(user=self.user_1, movie_id='Id_1')
        fav_movie_2 = FavouriteMovie.objects.create(user=self.user_2, movie_id='Id_2')
        fav_movie_3 = FavouriteMovie.objects.create(user=self.user_2, movie_id='Id_3')
        url = reverse('movie:favouritemovie-list')
        self.client.force_authenticate(self.user_2)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        favourite_movie_ids_in_response = [elem['id'] for elem in response.data]
        self.assertIn(fav_movie_2.id, favourite_movie_ids_in_response)
        self.assertIn(fav_movie_3.id, favourite_movie_ids_in_response)
        self.assertNotIn(fav_movie_1.id, favourite_movie_ids_in_response)


class TestMovieToWatchViewSetAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = get_user_model().objects.create(username='user1', password='password_1')
        cls.user_2 = get_user_model().objects.create(username='user2', password='password_2')

    def test_user_can_add_movie_to_watch(self):
        payload = {
            'movie_id': 'tt123456789'
        }
        url = reverse('movie:movietowatch-list')
        self.client.force_authenticate(self.user_1)

        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(payload['movie_id'], MovieToWatch.objects.get(pk=response.data['id']).movie_id)

    def test_user_cant_add_one_movie_twice(self):
        payload = {
            'movie_id': 'tt123456789'
        }
        url = reverse('movie:movietowatch-list')
        self.client.force_authenticate(self.user_1)

        self.client.post(url, payload)
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_user_who_create_movie_to_watch_can_delete_it(self):
        movie_1 = MovieToWatch.objects.create(user=self.user_1, movie_id='Id_1')
        MovieToWatch.objects.create(user=self.user_2, movie_id='Id_2')
        movie_1_url = reverse('movie:movietowatch-detail', kwargs={'pk': movie_1.pk})
        self.client.force_authenticate(self.user_2)

        response = self.client.delete(movie_1_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_field_is_not_taken_from_request(self):
        payload = {
            'movie_id': 'tt123456789',
            'user': self.user_2.pk,
        }
        url = reverse('movie:movietowatch-list')
        self.client.force_authenticate(self.user_1)

        response_1 = self.client.post(url, payload)

        self.assertEqual(MovieToWatch.objects.get(id=response_1.data['id']).user, self.user_1)
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)

    def test_list_show_only_logged_in_user_movie_to_watch(self):
        movie_1 = MovieToWatch.objects.create(user=self.user_1, movie_id='Id_1')
        movie_2 = MovieToWatch.objects.create(user=self.user_2, movie_id='Id_2')
        movie_3 = MovieToWatch.objects.create(user=self.user_2, movie_id='Id_3')
        url = reverse('movie:movietowatch-list')
        self.client.force_authenticate(self.user_2)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        movie_to_watch_ids_in_response = [elem['id'] for elem in response.data]
        self.assertIn(movie_2.id, movie_to_watch_ids_in_response)
        self.assertIn(movie_3.id, movie_to_watch_ids_in_response)
        self.assertNotIn(movie_1.id, movie_to_watch_ids_in_response)


class TestReviewViewSetAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = get_user_model().objects.create(username='user1', password='password_1')
        cls.user_2 = get_user_model().objects.create(username='user2', password='password_2')

    def test_user_can_add_review(self):
        payload = {
            'movie_id': 'tt123456789',
            'rating': '3',
            'review': 'My review'
        }
        url = reverse('movie:review-list')
        self.client.force_authenticate(self.user_1)

        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(payload['movie_id'], Review.objects.get(pk=response.data['id']).movie_id)

    def test_user_who_create_review_can_change_it(self):
        review_1 = Review.objects.create(user=self.user_1, movie_id='Id_1', rating=3)
        payload = {
            'movie_id': 'Id_1',
            'rating': '9',
            'review': 'My review'
        }
        Review.objects.create(user=self.user_2, movie_id='Id_2', rating=3)
        review_1_url = reverse('movie:review-detail', kwargs={'pk': review_1.pk})
        self.client.force_authenticate(self.user_2)

        response = self.client.put(review_1_url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cant_add_review_for_one_movie_twice(self):
        payload = {
            'movie_id': 'tt123456789',
            'rating': '3',
            'review': 'My review'
        }
        url = reverse('movie:review-list')
        self.client.force_authenticate(self.user_1)

        self.client.post(url, payload)
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_user_who_create_review_can_delete_it(self):
        review_1 = Review.objects.create(user=self.user_1, movie_id='Id_1', rating=3)
        Review.objects.create(user=self.user_2, movie_id='Id_2', rating=3)
        review_1_url = reverse('movie:review-detail', kwargs={'pk': review_1.pk})
        self.client.force_authenticate(self.user_2)

        response = self.client.delete(review_1_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_field_is_not_taken_from_request(self):
        payload = {
            'movie_id': 'tt123456789',
            'user': self.user_2.pk,
            'rating': '3',
            'review': 'My review'
        }
        url = reverse('movie:review-list')
        self.client.force_authenticate(self.user_1)

        response = self.client.post(url, payload)

        self.assertEqual(Review.objects.get(id=response.data['id']).user, self.user_1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_return_all_users_reviews(self):
        Review.objects.create(user=self.user_1, movie_id='Id_1', rating=3)
        Review.objects.create(user=self.user_1, movie_id='Id_2', rating=4)
        Review.objects.create(user=self.user_2, movie_id='Id_3', rating=10)

        url = reverse('movie:review-list')
        self.client.force_authenticate(self.user_1)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_by_user(self):
        review_1 = Review.objects.create(user=self.user_1, movie_id='Id_1', rating=3)
        review_2 = Review.objects.create(user=self.user_1, movie_id='Id_2', rating=4)
        review_3 = Review.objects.create(user=self.user_2, movie_id='Id_3', rating=10)
        url = reverse('movie:review-list') + f'?user={self.user_2.id}'
        self.client.force_authenticate(self.user_1)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        review_ids_in_response = [elem['id'] for elem in response.data]
        self.assertIn(review_3.id, review_ids_in_response)
        self.assertNotIn(review_1.id, review_ids_in_response)
        self.assertNotIn(review_2.id, review_ids_in_response)

    def test_filter_by_movie_id(self):
        review_1 = Review.objects.create(user=self.user_1, movie_id='Id_1', rating=3)
        review_2 = Review.objects.create(user=self.user_2, movie_id='Id_1', rating=4)
        review_3 = Review.objects.create(user=self.user_2, movie_id='Id_2', rating=10)
        url = reverse('movie:review-list') + '?movie_id=Id_1'
        self.client.force_authenticate(self.user_1)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        review_ids_in_response = [elem['id'] for elem in response.data]
        self.assertIn(review_1.id, review_ids_in_response)
        self.assertIn(review_2.id, review_ids_in_response)
        self.assertNotIn(review_3.id, review_ids_in_response)


class TestMovieViewSet(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(username='user1', password='password_1')

    def test_title_required(self):
        url = reverse('movie:movie-list')
        self.client.force_authenticate(self.user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('movies.views.Omdb_API.search_movies')
    def test_search(self, mock_search_movies):
        mock_search_movies.return_value = 'My value'

        url = reverse('movie:movie-list') + '?title=bird&genre=Horror'
        self.client.force_authenticate(self.user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_search_movies.assert_called_once_with(genre='Horror', title='bird')
        self.assertIn('My value', response.data)
