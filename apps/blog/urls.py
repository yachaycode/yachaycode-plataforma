from django.conf.urls import url
# para poder importar las imagenes
from .views import (Blog, Detalle_blog, buscador_blog,
					buscador_categoria, AcercaDe)
# from views import Usuarios
from django.conf import settings
from django.urls import path, include

# from django.views.static.
urlpatterns = [
    # url(r'^usuarios', Usuarios.as_view(), name='inicio'),
    # cuidado con esto tiene GRUD de Usuarios
    # url(r'^$', UsuarioVer.as_view(), name='p_inicio'),
    
    url(r'^$', Blog.as_view(),
        name='p_inicio'),
    url(r'^buscador/$', buscador_blog, name='p_buscador_blog'),
    url(r'^acerca/$', AcercaDe.as_view(), name='p_acerca_de'),
    url(r'^buscador/categorias/(?P<slug>[^/]+)/$',
        buscador_categoria, name='p_buscador_categoria'),
    url(r'^(?P<slug>[^/]+)/$',
        Detalle_blog.as_view(), name='p_detalle_blog'),
    
]
