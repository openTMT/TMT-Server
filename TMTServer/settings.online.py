import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING:  the secret key used in production secret!
SECRET_KEY = 'ty%o)9w26&bq2s9d5+8m9==k1$4a+@%0d#$*ya14g(oui4$4y7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_swagger',
    'tmtapp',
    'websocket',
    'channels',
    'iosapp',
    'userapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TMTServer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'TMTServer.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tmt',
        'USER': 'tmt',
        'PASSWORD': '1qaz2wsx',
        'HOST': '172.31.244.199',
        'PORT': '23306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

SESSION_COOKIE_NAME = 'TMTServer_session_id'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 29  # 29天cookie失效，配合禅道的过期时间

SESSION_COOKIE_SAMESITE = None


# # 跨域增加忽略
CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_ALLOW_ALL = False
#
# CORS_ORIGIN_WHITELIST = (
#     'localhost:8080',
# )

CORS_ALLOW_CREDENTIALS = True

# REST_FRAMEWORK = {
#     'DEFAULT_PARSER_CLASSES': (
#         'rest_framework.parsers.JSONParser',
#     )
# }


REST_FRAMEWORK = {

    'EXCEPTION_HANDLER': 'TMTServer.exceptions.custom_exception_handler',

    'DEFAULT_PERMISSION_CLASSES': [
        'TMTServer.permissions.CustomerPermission',
    ],

    'DEFAULT_PAGINATION_CLASS': 'TMTServer.pagination.LimitOffsetPaginationCustomer',
    'PAGE_SIZE': 10,
}

# channels配置
ASGI_APPLICATION = 'TMTServer.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# 上传文件最大尺寸
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 100  # 100MB

# 禅道地址
ZENTAO_HOST = 'http://zentao.opentmt.com/zentao'

# 自己的域名
DOMAIN = 'http://tmt-server.opentmt.com'
