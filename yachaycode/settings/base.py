import os
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# connect config.json
BASE_DIR_DB = (os.path.dirname(os.path.abspath(__file__)))
fileConfig = (BASE_DIR_DB+'/config.json')
with open(fileConfig) as data_file:    
    dataConfig = json.load(data_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = dataConfig.get('secret_key').get('key')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    # para comentarios discus
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.users',
    'social_django',
    'django_extensions',
    'import_export',
    # 'pagedown',
    # 'markdown_deux',
    'apps.blog',
    'apps.seo',
    'disqus',
    'martor'
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # para autenticacion con redes sociales
    'social_django.middleware.SocialAuthExceptionMiddleware',

]

ROOT_URLCONF = 'yachaycode.urls'

# para imprimir todo en la consola, bueno para hacer las pruebas
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Envio en verdad a un Correo
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# COMMENT DISCUS
DISQUS_API_KEY = dataConfig.get('disqus').get('api_key')
DISQUS_WEBSITE_SHORTNAME = dataConfig.get('disqus').get('website_shortname')

# para login y de paso reutilizaremos para autenticacion con redes sociales
LOGIN_URL = 'iniciar_sesion'  #estamos llamando por su name del Url no por su URL
LOGOUT_URL = 'cerrar_sesion'
LOGIN_REDIRECT_URL = 'index_principal'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# para autenticacion con redes sociales FB y TWITTER
AUTHENTICATION_BACKENDS = (
    # mi propio class para autenticacion por User o Email
    'apps.users.functions.UsernameOrEmailBackend',
    # autenticacion con redes sociales
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)


WSGI_APPLICATION = 'yachaycode.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# Conection db mongodb
DATABASES = {
    'default': {
        'ENGINE': dataConfig.get('db-connection').get('engine'),
        'NAME': dataConfig.get('db-connection').get('name'),
        'USER': dataConfig.get('db-connection').get('user'),
        'PASSWORD': dataConfig.get('db-connection').get('password'),
        'HOST': dataConfig.get('db-connection').get('host'),
        'PORT': dataConfig.get('db-connection').get('port')
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# MODIFICANDO EL SETTIING
AUTH_USER_MODEL = 'users.user'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'apps/blog/static'),
)
STATIC_URL = '/static/'

# esto al parecer es importane pero al momento todo funciona bien
# en cado de generar o copiar a otro directorio lo habilitamos esto con
# ./manage.py collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'public/static')

# MEDIA_ROOT = '/home/alejandro/sicoas/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'public/media')
MEDIA_URL = '/media/'


# personalizando django SOIT, template para admin 
SUIT_CONFIG = {
    'ADMIN_NAME': 'ADMINISTRATOR - YACHAYCODE',
    'HEADER_DATE_FORMAT': 'l, j. F Y', # Saturday, 16th March 2013
    'HEADER_TIME_FORMAT': 'H:i',     # 18:42
    'SHOW_REQUIRED_ASTERISK': True,
    'CONFIRM_UNSAVED_CHANGES': True,
    'MENU_OPEN_FIRST_CHILD': True,
    # falta algo, para buscar un cierto usuario
    'SEARCH_URL': '/admin/users/',
}
