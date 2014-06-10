from django.core.urlresolvers import reverse_lazy

# Base Configuration
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_URLCONF = 'taskrp.urls'
WSGI_APPLICATION = 'taskrp.wsgi.application'
STATIC_URL = '/static/'

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Security Configuration
SECRET_KEY = '#n#pf-*)rn3^1!lz854@w+ppr%gq7+g1&(dg*!*34s4l0=1uq2'
DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['*']

# Installed applications
INSTALLED_APPS = (
    # Django and django-related apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps
    'debug_toolbar',
    'south',
    'rest_framework',
    'bootstrap3',

    # 1st party apps
    'accounts',
    'taskr',
    'taskr_rest',
)

# Middleware Configuration
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Template Processor Configuration
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

# Auth Configuration
from django.conf.global_settings import AUTHENTICATION_BACKENDS as AUTHB
AUTHENTICATION_BACKENDS = ('accounts.backends.EmailIdentityBackend', ) + AUTHB
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = reverse_lazy('taskr:auth-login')
LOGOUT_URL = reverse_lazy('taskr:auth-logout')
LOGIN_REDIRECT_URL = reverse_lazy('taskr:index')

# Datetime Configuration
from django.conf.global_settings import DATETIME_INPUT_FORMATS as DIF
DATETIME_INPUT_FORMATS = (
    '%Y/%m/%d %H:%M',        # '2006/10/25 14:30'
    '%Y/%m/%d',              # '2006/10/25'
    '%y/%m/%d %H:%M',        # '06/10/25 14:30'
    '%y/%m/%d',              # '06/10/25'
) + DIF


## Third party settings
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