from django.contrib import admin
from import_export import resources
from .models import Blog, Categoria, ContadorVisita
from import_export.admin import ImportExportModelAdmin
from pagedown.widgets import AdminPagedownWidget
from django.db import models
# Register your models here.


class Blog_resource(resources.ModelResource):

    class Meta:
        model = Blog
        exclude = ()

class Blog_admin(ImportExportModelAdmin):
	filter_horizontal = ('categorias', 'posts_relacionados')
	search_fields = ('titulo','resumen',
				'fecha_publicacion','autor__perfil_usuario__nombres',
				'autor__perfil_usuario__apellidos', 'palabras_clave')
	list_display = ('titulo','resumen',
				'fecha_publicacion','autor','vistas',
				'estado',)
	list_editable = ('estado',)
	resource_class = Blog_resource
	formfield_overrides = {
            models.TextField: {'widget': AdminPagedownWidget},
        }


class Categoria_resource(resources.ModelResource):

    class Meta:
        model = Categoria
        exclude = ()


class Categoria_admin(ImportExportModelAdmin):
    resource_class = Categoria_resource


class ContadorVisita_resource(resources.ModelResource):

    class Meta:
        model = ContadorVisita
        exclude = ()


class ContadorVisita_admin(ImportExportModelAdmin):
	list_display = ('blog','contador','fecha_visita')
	search_fields = ('blog__titulo',)
	resource_class = ContadorVisita_resource

admin.site.register(Categoria, Categoria_admin)
admin.site.register(Blog, Blog_admin)
admin.site.register(ContadorVisita, ContadorVisita_admin)

