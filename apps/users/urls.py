from django.conf.urls import url
# para poder importar las imagenes
from django.views.static import serve
from .views import *
# from views import Users
from django.conf import settings

# from django.views.static.
urlpatterns = [
    # url(r'^usuarios', Users.as_view(), name='inicio'),
    # cuidado con esto tiene GRUD de Users
    # url(r'^$', UserVer.as_view(), name='p_inicio'),
    url(r'^nuevo/$', User_crear.as_view(),
        name='pu_nuevo'),
    url(r'^editar/(?P<pk>\d+)$',
        UserEditar.as_view(), name='p_editar'),
    url(r'^eliminar/(?P<pk>\d+)$',
        UserEliminar.as_view(), name='p_eliminar'),
    url(r'^cambio_contrasena$', change_password,
        name='change_password'),
    url(r'^contrasena$', cambio_contrasena,
        name='p_cambio_contrasena'),
    url(r'^(?P<usuario>[^/]+)$', Ver_perfil.as_view(),
        name='p_ver_perfil'),
    url(r'^(?P<usuario>[^/]+)/editar$', Editar_perfil.as_view(),
        name='p_editar_perfil'),
    url(r'^(?P<usuario>[^/]+)/cuenta$', Cuenta_usuario.as_view(),
        name='p_cuenta'),
    url(r'^cambiar_cuenta_usuario/$', Cambiar_cuenta_usuario.as_view(),
        name='p_cambiar_cuenta_usuario'),
    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
