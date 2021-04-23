from django.conf.urls import url, include
# para poder importar las imagenes
from .views import (Blog, Detalle_blog, buscador_blog,
					buscador_categoria, AcercaDe, contador_visitas, tags)
# from views import Usuarios
from django.conf import settings

# from django.views.static.
urlpatterns = [
    # url(r'^usuarios', Usuarios.as_view(), name='inicio'),
    # cuidado con esto tiene GRUD de Usuarios
    # url(r'^$', UsuarioVer.as_view(), name='p_inicio'),
    url(r'api/', include(('apps.blog.api.blog.urls', 'api_blog'), namespace='api_blog')),
    url(r'^$', Blog.as_view(),
        name='p_inicio'),
    url(r'^buscador/$', buscador_blog, name='p_buscador_blog'),
    url(r'^contador-visitas-ajax/$', contador_visitas, name='p_contador_visitas'),
    url(r'^acerca/$', AcercaDe.as_view(), name='p_acerca_de'),
    url(r'^tags/(?P<slug>[^/]+)/$', tags, name='p_tag_blog'),
    url(r'^buscador/categorias/(?P<slug>[^/]+)/$',
        buscador_categoria, name='p_buscador_categoria'),
    url(r'^(?P<slug>[^/]+)/$', Detalle_blog.as_view(), name='p_detalle_blog'),
    
]
