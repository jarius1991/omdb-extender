from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'},
                'min_length': 5,
            }
        }

    def create(self, validated_data):
        user_model = get_user_model()
        username = validated_data['username']
        email = user_model.objects.normalize_email(validated_data['email'])
        password = validated_data['password']

        user = user_model(username=username, email=email)
        user.set_password(password)
        user.save()
        return user
