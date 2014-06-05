__author__ = 'Alej. N. Pérez'


from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse_lazy, NoReverseMatch
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    """ Custom user manager for our model """
    def _create_user(self, email: str, password: str, is_staff: bool, is_superuser: bool, **extra_fields: dict) -> User:
        """ Inner abstract method for easy user creation """
        now = timezone.now()
        if not email:
            raise ValueError('email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_active=True,
                          last_login=now,
                          date_joined=now,
                          is_staff=is_staff,
                          is_superuser=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str=None, **extra_fields: dict):
        """ Create a normal user, with no privileges """
        return self._create_user(email=email,
                                 password=password,
                                 is_staff=False,
                                 is_superuser=False,
                                 **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields: dict):
        """ Create a superuser, a user with admin privileges """
        return self._create_user(email=email,
                                 password=password,
                                 is_staff=True,
                                 is_superuser=True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """ The custom User model defined for our module """
    # Required fields by AbstractBaseUser
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Model fields
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # Model manager
    objects = UserManager()

    # Model settings
    absolute_url = getattr(settings, 'ACCOUNTS_ABSOLUTE_URL', None)

    # Model metadata
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self) -> str:
        """ Returns the full name of the user, in this case the email """
        return self.email

    def get_short_name(self) -> str:
        """ Returns the short name of the user, in this case it's full name """
        return self.get_full_name()

    def get_absolute_url(self) -> str:
        """ Return the absolute url that identifies this user """
        if self.absolute_url is None:
            return '/accounts/user/%(id)s' % {'id': self.id}
        try:
            reversed_url = reverse_lazy(self.absolute_url)
        except NoReverseMatch:
            reversed_url = self.absolute_url
        return reversed_url