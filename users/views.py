from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, authenticate

from .serializers import UserSerializer
from .utils import check_User

User = get_user_model()


@api_view(['POST'])
def create_User(request):
    data = request.data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    value = check_User(username, password, email)
    if value:
        return value
    user = User.objects.create(
        username=username,
        email=email
    )    

    user.set_password(password)
    user.save()
    serializer = UserSerializer(user)
    data = serializer.data
    token, created = Token.objects.get_or_create(user=user)
    data['token'] = token.key
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_User(request):
    if not request.user.is_authenticated:
        detail = {
            'detail': 'Authentication credintals were not provided.'
        }
        return Response(detail, status=status.HTTP_401_UNAUTHORIZED)
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_Token(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        detail = {
            'detail': 'please send the username and the password.'
        }
        return Response(detail, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, username=username)
    user = authenticate(username=username, password=password)
    if not user:
        detail = {
            'detail': 'No User matches the given query.'
        }
        return Response(detail, status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user=user)
    detail = {
        'token': f'{token}'
    }
    return Response(detail, status=status.HTTP_200_OK)