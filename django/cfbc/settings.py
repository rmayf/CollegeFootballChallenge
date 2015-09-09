"""
Django settings for cfbc project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7q85t81iei_-w$r)c2u%&=57l^l53fxl2n+1c0d6e+6vjiz(_p'

import PrivateSettings as private

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = private.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = private.EMAIL_HOST_PASSWORD
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'Pac-12 Football Challenge'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

REST_FRAMEWORK = {
   'DEFAULT_PERMISSION_CLASSES' : [
      'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'  
   ]
}

#LOGIN_REDIRECT_URL = '/'
LOGIN_URL          = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = private.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY 
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = private.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET 
SOCIAL_AUTH_FACEBOOK_KEY = private.SOCIAL_AUTH_FACEBOOK_KEY
SOCIAL_AUTH_FACEBOOK_SECRET = private.SOCIAL_AUTH_FACEBOOK_SECRET
SOCIAL_AUTH_TWITTER_KEY = private.SOCIAL_AUTH_TWITTER_KEY 
SOCIAL_AUTH_TWITTER_SECRET = private.SOCIAL_AUTH_TWITTER_SECRET 


# Application definition

INSTALLED_APPS = (
    'registration',
    'week1',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chat',
    'stats',
    'leaderboard',
    'rest_framework',
    'rest_framework.authtoken',
    'social.apps.django_app.default',
)

ACCOUNT_ACTIVATION_DAYS = 7

AUTHENTICATION_BACKENDS = (
   'django.contrib.auth.backends.ModelBackend',
   'social.backends.twitter.TwitterOAuth',
   'social.backends.facebook.FacebookOAuth2',
   'social.backends.google.GoogleOAuth2',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'cfbc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join( BASE_DIR, 'cfbc/templates' ) ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

#TEMPLATE_DIRS = (
#   os.path.join(BASE_DIR, 'templates'),
#)

WSGI_APPLICATION = 'cfbc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
