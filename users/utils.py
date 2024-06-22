from rest_framework.response import Response
from rest_framework import status 


from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

def check_User(username, password, email):
    if not username or not password or not email:
        return Response({'errors': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.filter(username=username)
    if user.exists():
        return Response({'errors': 'This name is used before.'}, status=status.HTTP_400_BAD_REQUEST)

    if not email.endswith('@gmail.com'):
        return Response({'errors': "the email should end with '@gmail.com'."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        validate_password(password)
    except ValidationError as e:
        return Response({'errors': e.messages}, status=status.HTTP_400_BAD_REQUEST)
    

