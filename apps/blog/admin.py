from django.contrib import admin
from import_export import resources
from .models import Blog, Categoria
from import_export.admin import ImportExportModelAdmin
from pagedown.widgets import AdminPagedownWidget
from django.db import models
# Register your models here.


class Blog_resource(resources.ModelResource):

    class Meta:
        model = Blog
        exclude = ()

class Blog_admin(ImportExportModelAdmin):
	filter_horizontal = ('categorias',)
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

admin.site.register(Categoria, Categoria_admin)
admin.site.register(Blog, Blog_admin)

