
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import environ
env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')
print("--- RUNING IN >>> %s <<< MODE ---" % ("DEBUG" if DEBUG else "RELEASE"))

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "voting",
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

ROOT_URLCONF = 'zumba.urls'

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
                'voting.wechat.wechat_ctx',
            ],
        },
    },
]

WSGI_APPLICATION = 'zumba.wsgi.application'


DATABASES = {
    'default': env.db(),
}


LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False


STATIC_ROOT = env("STATIC_ROOT")
STATIC_URL =  env("STATIC_URL")
MEDIA_ROOT = env("MEDIA_ROOT")
MEDIA_URL =  env("MEDIA_URL")


CACHES = {'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    "voting.backend.ZumbaBackend",
)

LOGIN_URL = env('LOGIN_URL')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] [%(name)s:%(lineno)d] [%(levelname)s]: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '[%(name)s:%(lineno)d] [%(levelname)s]: %(message)s'
         },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        "zumba": {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        "django.db.backends": {
            'level': 'INFO',
            'handlers':['console'],
        }
    },
}

ZUMBA_APPID = env("ZUMBA_APPID")
ZUMBA_SECRET = env("ZUMBA_SECRET")
ZUMBA_UINFO_URL = env("UINFO_URL")

