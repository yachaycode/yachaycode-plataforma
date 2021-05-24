# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django import forms
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):

    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __unicode__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = User
        fields = ("username",)


class CustomUserChangeForm(UserChangeForm):

    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __unicode__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = User
        fields = ("username",)
        exclude = ()


class UserForm(forms.ModelForm):

    # validacion del correo a nivel del form
    # def clean(self):
    #     consulta = User.objects.filter(email=self.cleaned_data.get('email')).exists()
    #     if consulta:
    #         raise ValidationError("Ya existe un User con este correo")
    #     return self.cleaned_data
    class Meta:
        model = User
        exclude = ('date_joined', 'is_staff',
                   'is_active', 'is_superuser')
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control',
                'pattern': '[a-zA-Z0-9ñÑáéíóúÁÉÍÓÚüÜ.-_]{2,35}',
                'title': "No es un formato válido, revise por favor..!"}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            # 'date_joined': forms.TextInput(attrs={'class': 'form-control'}),
        }

# para cambiar name de USUARIO
class UserForm_usaurio(forms.ModelForm):

    class Meta:
        model = User
        exclude = ('date_joined', 'is_staff',
                   'is_active', 'is_superuser','password')
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control',
                'pattern': '[a-zA-Z0-9ñÑáéíóúÁÉÍÓÚüÜ.-_]{2,35}',
                'title': "No es un formato válido, revise por favor..!",
                'placeholder': 'Ususario',
                'id': 'id_user_register'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control',
                'placeholder': 'Correo electronico'}),
            # 'date_joined': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('fecha_nacimiento',)
        widgets = {
            # 'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            # 'dni': forms.TextInput(attrs={'class': 'form-control',
            #                               'data-rule-minlength': '8',
            #                               'data-rule-maxlength': '8',
            #                               'title': "Solo esta permitido NUMEROS 8 dígitos de 0 al 9..!",
            #                               'autocomplete': 'off',
            #                               'autocorrect': 'off'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control',
                'pattern': '[a-zA-ZñÑáéíóúÁÉÍÓÚüÜ a-zA-ZñÑáéíóúÁÉÍÓÚüÜ]{2,60}',
                'title': "No es un formato válido, revise por favor..!",
                'autocomplete': 'off',
                'autocorrect': 'off'}),
            # 'readonly': 'readonly'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control',
                'pattern': "[a-zA-ZñÑáéíóúÁÉÍÓÚüÜ a-zA-ZñÑáéíóúÁÉÍÓÚüÜ]{2,45}",
                'autocomplete': 'off',
                'autocorrect': 'off'}),
            # 'readonly': 'readonly'}),
            'cellphone': forms.TextInput(
                attrs={'class': 'form-control',
                'maxlength': '9',
                'pattern':'\d*',
                'title': "Solo esta permitido NUMEROS 9 dígitos de 0 al 9..!"}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'username': forms.HiddenInput(),
        }


class UserProfileEditForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('username', 'country_code')
        widgets = {
            # 'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            # 'dni': forms.TextInput(attrs={'class': 'form-control',
            #                               'data-rule-minlength': '8',
            #                               'data-rule-maxlength': '8',
            #                               'title': "Solo esta permitido NUMEROS 8 dígitos de 0 al 9..!",
            #                               'autocomplete': 'off',
            #                               'autocorrect': 'off'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control',
                'pattern': '[a-zA-ZñÑáéíóúÁÉÍÓÚüÜ a-zA-ZñÑáéíóúÁÉÍÓÚüÜ]{2,60}',
                'title': "No es un formato válido, revise por favor..!",
                'autocomplete': 'off',
                'autocorrect': 'off'}),
            # 'readonly': 'readonly'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control',
                'pattern': "[a-zA-ZñÑáéíóúÁÉÍÓÚüÜ a-zA-ZñÑáéíóúÁÉÍÓÚüÜ]{2,45}",
                'autocomplete': 'off',
                'autocorrect': 'off'}),
            # 'readonly': 'readonly'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'capture': 'camera'}),
            'cellphone': forms.TextInput(
                attrs={'class': 'form-control',
                'maxlength': '9',
                'pattern':'\d*',
                'title': "Solo esta permitido NUMEROS 9 dígitos de 0 al 9..!"}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'profesion': forms.TextInput(attrs={'class': 'form-control'}),
            # me parece que solo con material desing funciona style
            'biography': forms.Textarea(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'data-rule-email': 'true'}),
            'fecha_nacimiento': forms.DateTimeInput(attrs={'class': 'form-control'})
        }
