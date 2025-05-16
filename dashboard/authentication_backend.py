from django.contrib.auth.backends import BaseBackend
from attendance.models import Admin
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class AdminBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            admin = Admin.objects.get(username=username)
            if check_password(password, admin.password_hash):
                # Create a dummy user object to use Django's authentication system
                user = User(username=admin.username, is_staff=True, is_superuser=True)
                user.id = admin.id  # Map the ID to the Admin table
                return user
        except Admin.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            admin = Admin.objects.get(id=user_id)
            # Create a dummy user object
            user = User(username=admin.username, is_staff=True, is_superuser=True)
            user.id = admin.id
            return user
        except Admin.DoesNotExist:
            return None
