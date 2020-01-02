from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from rest_framework.test import APITestCase
from rest_framework import status

CREATE_LIST_USER_URL = reverse('user:create-list-user')
TOKEN_URL = reverse('user:token')


class PublicUserApiTests(APITestCase):
    """Test the user API (public)"""

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'username': 'test_name',
            'email': 'test@website.com',
            'password': 'test_password',
        }

        res = self.client.post(CREATE_LIST_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """"Test creating a user that already exists"""
        payload = {
            'username': 'Test name',
            'email': 'test@website.com',
            'password': 'password123',
        }
        get_user_model().objects.create_user(**payload)

        res = self.client.post(CREATE_LIST_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'username': 'test_name',
            'email': 'test@website.com',
            'password': 'pa',
        }
        res = self.client.post(CREATE_LIST_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(username=payload['username']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that the token is created for the user"""
        payload = {'username': 'test_username', 'password': 'test_pass'}
        get_user_model().objects.create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        get_user_model().objects.create_user(username='test_username', password='test_pass')

        payload = {'username': 'test_username', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {
            'username': 'no_user',
            'password': 'test_pass',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        get_user_model().objects.create_user(username='test_username', password='test_pass')
        res = self.client.post(TOKEN_URL, {'username': 'test_username', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
