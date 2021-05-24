from django.contrib.auth import authenticate, login
from django.db.models import Q
from .models import User
from django.contrib.auth.backends import ModelBackend

# esto es sumamente importante, que nos va permitir iniciar por correo o usuario
# por defecto django tiene USERNAME_FIELD = 'username', basicamente para redes
# sociales es debe quedar aqui, y aqui forzamos que inice por email


class UsernameOrEmailBackend(ModelBackend):

    def authenticate(self, email=None, password=None, **kwargs):
        try:
            # autenticacion por usuario y email
            user = User.objects.get(Q(username=email) | Q(email=email))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            User().set_password(password)
