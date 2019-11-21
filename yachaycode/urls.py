"""yachaycode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.users.views import (change_password, 
                                        registro_usuario_modals, 
                                        Completar_registro_perfil,
                                        Registrarse, Index_principal,
                                        LogOut, userlogin,
                                        activate)
from apps.users import views as core_views
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', Index_principal.as_view(), name="index_principal"),
    path(r'oauth/', include('social_django.urls', namespace='social')),
    path(r'usuarios/', include(('apps.users.urls', 'app_usuarios'), 
        namespace='app_usuarios')),
    path(r'blog/', include(('apps.blog.urls', 'app_blog'), 
        namespace='app_blog')),
    path(r'settings/', core_views.settings, name='settings'),
    path(r'settings/password/', core_views.password, name='password'),
    path(r'iniciar/', userlogin, name="iniciar_sesion"),
    path(r'salir/', LogOut, name='cerrar_sesion'),
        # para recuperacion de contraseña
    path('', include('django.contrib.auth.urls')),
    path(r'registrarse/', Registrarse.as_view(), 
        name="registrarse_usuario"),
    path('martor/', include('martor.urls'))
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.views import serve as static_serve
    staticpatterns = static(settings.STATIC_URL, view=static_serve)
    mediapatterns = static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = staticpatterns + mediapatterns + urlpatterns
