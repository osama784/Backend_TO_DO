from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

unique_name = UniqueValidator(queryset=User.objects.all(), lookup='iexact')