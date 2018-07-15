from .base import *

DEBUG =  False


# PARA DETECCUION DE ERRORES CON SENTRY 
INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

RAVEN_CONFIG = {
    'dsn': 'https://12b47432335449d0aebba84cc6725a48@sentry.io/1243587',	
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    # 'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
}
