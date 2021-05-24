from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

# from .models import User, UserProfile, Testimonio, Terminos, Politicas
from .models import *
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .actions import export_as_csv

from import_export import resources
from import_export.admin import ImportExportModelAdmin
# from pagedown.widgets import AdminPagedownWidget

# Register your models here.
from django.contrib.auth.models import Group
# desregistramos GROUP para poder agregar IMMPORTAR E Exportar todos lo
# grupos GENERADOS
admin.site.unregister(Group)


class UserResource(resources.ModelResource):

    class Meta:
        model = User
        # fields = ('id',
        #           'username',
        #           'dni',
        #           'last_name',
        #           'first_name',
        #           'sexo',
        #           'cellphone',
        #           'email',
        #           'is_superuser',
        #           'is_staff',
        #           'is_active',
        #           'groups',
        #           'date_joined'
        #           )
        # exclude = ('password',
        #           'last_login',
        #           'user_permissions')
        exclude = ()


class UserAdminLocal(ImportExportModelAdmin):
    resource_class = UserResource


# Aqui integramos UserAdmin de todos los LISTAS de usuarios y
# UserAdmin para importar y exportar

# En este caso agregaremos en User su Perfil

class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil usuario'
    fk_name = 'user'
    # para agrgar solo un perfil, por defecto lo agregara varios
    # eso es lo que no queremos
    extra = 1
    # max 1, porque la relacion es 1 a 1
    max_num = 1
    min_num = 1


class CustomUserAdmin(UserAdmin, UserAdminLocal):

    # para agregar perfil de usuario a User
    inlines = (ProfileInline, )
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
         'fields': ('email',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
         ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('username', 'get_first_name', 'get_last_name', 'get_cellphone',
                    'get_country', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_active', 'groups__name')
    list_editable = ('is_active',)
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    actions = [export_as_csv, ]

    # relacionar con un name para poder acceder a sus atributos de perfil User
    # esto funcionara solo con relaciones OneToOneField
    list_select_related = ('userprofile', )

    # para agregar Perfil de User
    # para mostrar campos de perfil de User en Usario(list_display)

    def get_first_name(self, instance):
        return instance.userprofile.first_name
    get_first_name.short_description = 'Firt name'

    def get_last_name(self, instance):
        return instance.userprofile.last_name
    get_last_name.short_description = 'Last name'

    def get_cellphone(self, instance):
        return instance.userprofile.cellphone
    get_cellphone.short_description = 'cellphone'

    def get_country(self, instance):
        return instance.userprofile.country
    get_country.short_description = 'Country'

    # Mostrar con su perfil el usuario
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


# registrando los modelos en el admin

# para asignar importar e Exportar en GRUPOS
# para eventos
class GroupResource(resources.ModelResource):

    class Meta:
        model = Group
        exclude = ()


class GroupAdmin(ImportExportModelAdmin):
    resource_class = GroupResource
    filter_horizontal = ('permissions', )


class UserProfileResource(resources.ModelResource):

    class Meta:
        model = UserProfile
        exclude = ()


class UserProfileAdmin(ImportExportModelAdmin):
    list_display = ('user', 'first_name',
                    'last_name', 'cellphone', 'country',
                    'occupation')
    search_fields = ('first_name', 'last_name',
                     'cellphone', 'country')
    list_filter = ('country',)
    resource_class = UserProfileResource


admin.site.register(Group, GroupAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
