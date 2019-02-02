import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Make this variable True if you wish to develop
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECREY_KEY', '9^*+s+=^vg17!!4q5l!n*#9(i1+65(x9)k1@zl&ub+=@$!b-#2')

ALLOWED_HOSTS = (['127.0.0.1', 'localhost'] + [os.environ.get('DOMAIN_NAME','')])

USE_TZ = True
TIME_ZONE = "UTC"

if DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'build/static'),
    )
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'build/static')
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'build/static'),
    ]
    #STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'channels',
    'users',
    'api',
    'questions',
    'ohqueue',
    'frontend',
    'stats',
]

ASGI_APPLICATION = 'ohqueue.routing.application'

if DEBUG:
    CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
            },
        }
    }

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    if 'TRAVIS' in os.environ:
        EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    else:
        EMAIL_USE_TLS = True
        EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.sendgrid.net')
        EMAIL_HOST_USER = os.environ.get('EMAIL_USERNAME', 'username')
        EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD', 'password')
        EMAIL_PORT = 587
        DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "")

SITE_ID = 1

AUTH_USER_MODEL = 'users.StudentUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '50/day',
        'user': '1000/day'
    }
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ohqueue.middleware.ShibbolethMiddleware',
]

ROOT_URLCONF = 'ohq.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        os.path.join(BASE_DIR, 'build'),
        os.path.join(BASE_DIR, 'templates')
        ],
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

WSGI_APPLICATION = 'ohq.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else: 
    if 'TRAVIS' in os.environ:
        DATABASES = {
            'default': {
                'ENGINE':   'django.db.backends.postgresql_psycopg2',
                'NAME':     'travisci',
                'USER':     'postgres',
                'PASSWORD': '',
                'HOST':     'localhost',
                'PORT':     '',
            }
        }
    else:
        db_url = os.environ.get('DATABASE_URL', 'postgres://...')
        DATABASES = {"default": dj_database_url.config(default=db_url)}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
