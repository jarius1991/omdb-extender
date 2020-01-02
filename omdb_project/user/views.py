from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer


class CreateUserView(generics.ListCreateAPIView):
    """The view for creating and listing users"""
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class CreateTokenView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
