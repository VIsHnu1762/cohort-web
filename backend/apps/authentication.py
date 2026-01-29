from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q


class EmailOrUsernameBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in with either
    their email address or username.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to find user by email or username
            user = User.objects.get(Q(username=username) | Q(email=username))
            
            # Check if password is correct
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user
            User().set_password(password)
            return None
        except User.MultipleObjectsReturned:
            # In case there are multiple users with the same email
            user = User.objects.filter(Q(username=username) | Q(email=username)).order_by('id').first()
            if user and user.check_password(password):
                return user
            return None
