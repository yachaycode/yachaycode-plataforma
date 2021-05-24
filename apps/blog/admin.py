from django.contrib import admin
from import_export import resources
from .models import Blog, Category, VisitorCounter
from import_export.admin import ImportExportModelAdmin
# from pagedown.widgets import AdminPagedownWidget
from django.db import models
from martor.widgets import AdminMartorWidget
from apps.seo.models import SeoBlog
# Register your models here.


class SeoInline(admin.StackedInline):
    model = SeoBlog
    can_delete = False
    verbose_name_plural = 'Meta data'
    fk_name = 'blog'
    # para agregar solo un Seo, por defecto lo agregara varios
    # eso es lo que no queremos
    extra = 1
    # max 1, porque la relacion es 1 a 1
    max_num = 1
    min_num = 1

class BlogResource(resources.ModelResource):

    class Meta:
        model = Blog
        exclude = ()

class BlogAdmin(ImportExportModelAdmin):
	inlines = (SeoInline, )
	filter_horizontal = ('categories', 'related_posts')
	search_fields = ('title','summary',
				'created_at','author__userprofile__first_name',
				'author__userprofile__last_name', 'keywords')
	list_display = ('title','summary',
				'created_at','author','number_views',
				'status', 'is_main_article')
	list_editable = ('status', 'is_main_article')
	resource_class = BlogResource
	formfield_overrides = {
		models.TextField: {'widget': AdminMartorWidget},
    }


class CategoryResource(resources.ModelResource):

    class Meta:
        model = Category
        exclude = ()


class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource


class VisitorCounterResource(resources.ModelResource):

    class Meta:
        model = VisitorCounter
        exclude = ()


class VisitorCounterAdmin(ImportExportModelAdmin):
	list_display = ('blog','counter','created_date')
	search_fields = ('blog__title',)
	resource_class = VisitorCounterResource

admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(VisitorCounter, VisitorCounterAdmin)

