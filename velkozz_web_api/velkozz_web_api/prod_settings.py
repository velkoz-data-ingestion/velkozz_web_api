from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/


SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["0.0.0.0", "127.0.0.1", "localhost"]

# Url Path for Login Redirect:
LOGIN_REDIRECT_URL = '/'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party Apps:
    "rest_framework",
    "rest_framework.authtoken",
    "rest_auth",
    
    # Local Applications: 
    # The Custom User Accounts Application:
    "accounts.apps.UserAccountConfig",

    # The Social Media API Application:
    "social_media_api.apps.SocialMediaAPIConfig",

    # The Finance API Application:
    "finance_api.apps.FinanceApiConfig"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'velkozz_web_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(os.path.join(BASE_DIR, "templates"))], # Adding the templates directory for global templating.
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

WSGI_APPLICATION = 'velkozz_web_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ["POSTGRES_DB"],
        'USER': os.environ["POSTGRES_USER"],
        'PASSWORD': os.environ["POSTGRES_PASSWORD"],
        'HOST': "psql_db",
        'PORT': os.environ["POSTGRES_PORT"]

    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# REST API Framework Settings:
REST_FRAMEWORK = {

    # DRF Authentication:
    'DEFAULT_AUTHENTICATION_CLASSES': (
                'rest_framework.authentication.SessionAuthentication',
                'rest_framework.authentication.TokenAuthentication',
    ),

    # DRF Permissions:
    'DEFAULT_PERMISSION_CLASSES':(
                'rest_framework.permissions.IsAuthenticated',
    ),

    # DRF Throtteling:
    'DEFAULT_THROTTLE_CLASSES': [],
    'GROUP_THROTTLE_RATES': {
        
        'api_burst_free_tier' : '10/minute',
        'api_sus_free_tier' : '100/day',

        'api_burst_senior_tier' : '50/minute',
        'api_sus_senior_tier' : '200/day',

        'api_burst_professional_tier' : '100/minute',
        'api_sus_professional_tier' : '300/day',

        'api_burst_ingestion' : '10000/minuite',
        'api_sus_ingestion' : '100000/day',

        'api_burst_developer' : '10000/minuite',
        'api_sus_developer' : '100000/day'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticroot")

# Adding a global static directory to the app: 
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Development MEDIA_ROOT for static files:
MEDIA_ROOT = "static_files/"

# Pointing to the Custom User Model:
AUTH_USER_MODEL = "accounts.CustomUser"