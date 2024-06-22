from rest_framework import serializers

from django.contrib.auth import get_user_model

from .validators import unique_name

User = get_user_model()


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, validators=[unique_name])
    email = serializers.EmailField()
    