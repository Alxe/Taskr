"""
Django settings for TaskrP project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.core.urlresolvers import reverse_lazy
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '#n#pf-*)rn3^1!lz854@w+ppr%gq7+g1&(dg*!*34s4l0=1uq2'
ALLOWED_HOSTS = ['*']
DEBUG = True
TEMPLATE_DEBUG = True

# Auth settings
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = ('accounts.backends.EmailIdentityBackend', )

# Accounts (authentication module) settings
ACCOUNTS_NEXT_LOGIN = reverse_lazy('taskr:index')
ACCOUNTS_NEXT_LOGOUT = reverse_lazy('taskr:index')
ACCOUNTS_NEXT_REGISTER = reverse_lazy('taskr:index')

# Installed applications
INSTALLED_APPS = (
    # Django and django-related apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.staticfiles',

    # 1st party apps
    'accounts',
    'taskr',

    # 3rd party apps
    'south',
    'rest_framework',
    'bootstrap3',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'taskrp.urls'

WSGI_APPLICATION = 'taskrp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Login/Logout

LOGIN_REDIRECT_URL = 'taskr:index'
LOGIN_URL = 'taskr:auth_login'
LOGOUT_URL = 'taskr:auth_logout'

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

# Django-boostrap3
BOOTSTRAP3 = {
    'theme_url': '//netdna.bootstrapcdn.com/bootswatch/3.1.1/flatly/bootstrap.min.css',
    'horizontal_field_class': 'col-md-8',
}

# Django-REST-framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),
    'PAGINATE_BY': 10
}