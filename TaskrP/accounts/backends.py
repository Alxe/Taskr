from .models import User


class EmailIdentityBackend(object):
    """ Backend to provide authentication to our module's custom User """

    def authenticate(self, email=None, password=None):
        """ Return the user with the provided data, or None if not found """
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """ Returns a user given it's primary key, or None if not found"""
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None
