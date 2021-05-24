from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from django.conf import settings
from django.core.mail import send_mail

from django.core.exceptions import ValidationError
class CustomUserManager(BaseUserManager):

    # aqui falta agregar correo en caso de registrar correo por redes sociales
    # de momento solo estara disponible con username
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        email = self.normalize_email(email)
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        user, created = self.get_or_create(email=email)
        if created: 
            user.set_password(password)
            user.username=username
            user.last_login=now
            user.date_joined=now
            user.is_staff=is_staff
            user.is_active = True
            user.is_superuser = is_superuser
            user.save()
            grupo, created = Group.objects.get_or_create(name='Reader')
            # get_or_create() didn't have to create an object.
            user.groups.add(grupo)
            UserProfile.objects.create(user=user)
        else:
            # user.set_password(password)
            # user.username = username
            # user.is_staff = is_staff
            # user.is_active = True
            user.last_login = now
            # user.date_joined = now
            # user.is_superuser = is_superuser
            user.save()
        return user



    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(_('Username'), max_length=60, unique=True)
    email = models.EmailField(null=True, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    # importante porque activaremos con confirmacion de correo de registro
    is_active = models.BooleanField(_('active'), default=False,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = CustomUserManager()
    # cuidado solo el inicio de sesion esta configurado con correo:
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('Users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.username)    
        return (full_name.strip()) or u''

    def get_short_name(self):
        "Returns the short name for the user."
        return (self.username) or u''

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.username])


class UserProfile(models.Model):
    """docstring for UserProfile"""
    select_country = (
        ('Peru', 'Perú'),
        ('Bolivia', 'Bolivia'),
        ('Chile', 'Chile'),
        ('Ecuador', 'Ecuador'),
        ('Colombia', 'Colombia'),
        ('Argentina', 'Argentina'),
        ('Brasil', 'Brasil'),
        ('Mexico', 'Mexico'),
        ('Otros', 'Otros')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # dni = models.CharField(max_length=8, unique=True, null=True)
    first_name = models.CharField(max_length=120, null=True)
    last_name = models.CharField(max_length=80, null=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=(('M', 'male'), ('F', 'female')),
                            max_length=20, null=True, blank=True)
    photo = models.ImageField(upload_to='fotos_usernames',
                             default='fotos_usuarios/avatar.png', blank=True)
    cellphone = models.DecimalField(
        max_length=9, max_digits=9, decimal_places=0, null=True)
    country_code = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, choices=select_country, default='Peru')
    city = models.CharField(max_length=80, null=True)
    occupation = models.CharField(max_length=120, null=True, blank=True)
    profession = models.CharField(max_length=120, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    facebook= models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)

    def __str__(self):
        return str(self.user) or u''

    class Meta:
        verbose_name_plural = _('Users Profile')
        verbose_name = _('User Perfile')
