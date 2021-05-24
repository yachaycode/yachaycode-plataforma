from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView
from .models import Blog as Blogs, Category
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# para paginador
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.
class Blog(ListView):
    """docstring for ver_todas_tortas"""
    context_object_name = 'blogs'
    template_name = 'blog/blog.html'
    paginate_by = 12
    model = Blogs
    def get_context_data(self, *args, **kwargs):
        context_data = super(Blog, self).get_context_data(*args, **kwargs)
        # realizamos consulta de todos los categories de blogs
        blogs = Blogs.objects.filter(status=True).order_by('created_at')
        list_blogs = []
        for blog in blogs:
           dict_blog = {}
           dict_blog['title'] = blog.title
           dict_blog['slug'] = blog.slug
           dict_blog['summary'] = blog.summary[0:250] + '...' if len(blog.summary)>250 else blog.summary
           dict_blog['content'] = blog.content
           dict_blog['categories'] = blog.categories
           dict_blog['cover_image'] = blog.cover_image
           dict_blog['created_at'] = blog.created_at
           dict_blog['author'] = blog.author
           dict_blog['number_views'] = blog.number_views
           dict_blog['keywords'] = blog.keywords
           dict_blog['status'] = blog.status
           dict_blog['is_main_article'] = blog.is_main_article
           dict_blog['related_posts'] = blog.related_posts
           list_blogs.append(dict_blog)
        context_data['blogs'] = list_blogs
        context_data['categories_blog'] = Category.objects.all()

        return context_data

class Detalle_blog(DetailView):
    """docstring for Detalle_curso"""
    # ordenar los modulos segun el orden de creacion
    context_object_name = 'detalle_blog'
    template_name = "blog/detalle_blog.html"
    model = Blogs
    slug_field = 'slug'

    def get_domain(self):
        current_site = get_current_site(self.request)  
        if current_site.domain in ['localhost', 'example.com']:
            sheme = 'http://'
        else:
            sheme = 'https://'
        return sheme + current_site.domain

    def get_context_data(self, *args, **kwargs):
        context_data = super(Detalle_blog, self).get_context_data(*args, **kwargs)
        # realizamos consulta de todos los categories de blogs
        context_data['domain'] = self.get_domain()
        return context_data


def buscador_blog(request):


    """docstring for Busqueda"""
    # todo tipo de buscador siempre buscara con cualquier parámetro, 
    # siempre en cuando este status = TRUE, inidica que está activo
    consulta = request.GET.get('q', '')
    lista_blogs = None
    list_blogs = []
    if consulta:
        lista_blogs = Blogs.objects.filter(
            Q(title__icontains=consulta) |
            Q(summary__icontains=consulta) |
            Q(keywords__icontains=consulta) |
            Q(categories__name__icontains=consulta), status=True).distinct()
    # else:
        # en caso si alguien entra directamente a /busquedas
        # lista_blogs = Curso.objects.all().order_by('-fecha_creacion')[:2]
    # paginandor
        for blog in lista_blogs:
           dict_blog = {}
           dict_blog['title'] = blog.title
           dict_blog['slug'] = blog.slug
           dict_blog['summary'] = blog.summary[0:250] + '...' if len(blog.summary)>250 else blog.summary
           dict_blog['content'] = blog.content
           dict_blog['categories'] = blog.categories
           dict_blog['cover_image'] = blog.cover_image
           dict_blog['created_at'] = blog.created_at
           dict_blog['author'] = blog.author
           dict_blog['number_views'] = blog.number_views
           dict_blog['keywords'] = blog.keywords
           dict_blog['status'] = blog.status
           dict_blog['is_main_article'] = blog.is_main_article
           dict_blog['related_posts'] = blog.related_posts
           list_blogs.append(dict_blog)
    paginator = Paginator(list_blogs, 12)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blogs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blogs = paginator.page(paginator.num_pages)

    categories = Category.objects.all()

    return render(request, 'blog/buscador_blog.html',
                  {'blogs': blogs, 'categories': categories})


def buscador_categoria(request, slug):
    try:
        consulta = Blogs.objects.filter(
            categories__slug=slug, status=True)
        list_blogs = []
        for blog in consulta:
           dict_blog = {}
           dict_blog['title'] = blog.title
           dict_blog['slug'] = blog.slug
           dict_blog['summary'] = blog.summary[0:250] + '...' if len(blog.summary)>250 else blog.summary
           dict_blog['content'] = blog.content
           dict_blog['categories'] = blog.categories
           dict_blog['cover_image'] = blog.cover_image
           dict_blog['created_at'] = blog.created_at
           dict_blog['author'] = blog.author
           dict_blog['number_views'] = blog.number_views
           dict_blog['keywords'] = blog.keywords
           dict_blog['status'] = blog.status
           dict_blog['is_main_article'] = blog.is_main_article
           dict_blog['related_posts'] = blog.related_posts
           list_blogs.append(dict_blog)
        categories = Category.objects.all()
        return render(request, 'blog/buscador_blog.html',
                      {'blogs': list_blogs, 'categories': categories})
    except Exception as e:
        raise 

class AcercaDe(TemplateView):
    template_name = 'blog/nosotros.html'

@csrf_exempt 
def contador_visitas(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            status = False
            blog = get_object_or_404(Blogs, 
                status=True, pk=request.POST.get('id'))
            blog.number_views +=1
            blog.save()
            status = True
            response = JsonResponse({'status': status})
            return HttpResponse(response.content)            
        except Exception as e:
            print ("Error:", e)
            response = JsonResponse({'status': status, 'error': str(e)})
            return HttpResponse(response.content)            
    else:
        return redirect('/')

def tags(request, slug):
    try:
        consulta = Blogs.objects.filter(
            categories__slug=slug)
        categories = Category.objects.all()
        return render(request, 'blog/categories.html',
                      {'blogs': consulta, 'slug': slug})
    except Exception as e:
        raise e