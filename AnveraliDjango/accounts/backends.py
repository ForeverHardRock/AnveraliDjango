from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password

from .models import AllUsers
from django.core.exceptions import ObjectDoesNotExist


class NewBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = AllUsers.objects.get(username=username)
            if user and check_password(password, user.password):
                return user
        except ObjectDoesNotExist:
            return None

