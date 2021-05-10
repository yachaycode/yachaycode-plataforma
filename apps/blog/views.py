from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView
from .models import Blog as Blogs, Categoria
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
        # realizamos consulta de todos los categorias de blogs
        blogs = Blogs.objects.filter(estado=True).order_by('fecha_publicacion')
        list_blogs = []
        for blog in blogs:
           dict_blog = {}
           dict_blog['titulo'] = blog.titulo
           dict_blog['slug'] = blog.slug
           dict_blog['resumen'] = blog.resumen[0:250] + '...' if len(blog.resumen)>250 else blog.resumen
           dict_blog['contenido'] = blog.contenido
           dict_blog['categorias'] = blog.categorias
           dict_blog['portada'] = blog.portada
           dict_blog['fecha_publicacion'] = blog.fecha_publicacion
           dict_blog['autor'] = blog.autor
           dict_blog['vistas'] = blog.vistas
           dict_blog['palabras_clave'] = blog.palabras_clave
           dict_blog['estado'] = blog.estado
           dict_blog['es_pricipal'] = blog.es_pricipal
           dict_blog['posts_relacionados'] = blog.posts_relacionados
           list_blogs.append(dict_blog)
        context_data['blogs'] = list_blogs
        context_data['categorias_blog'] = Categoria.objects.all()

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
        # realizamos consulta de todos los categorias de blogs
        context_data['domain'] = self.get_domain()
        return context_data


def buscador_blog(request):


    """docstring for Busqueda"""
    # todo tipo de buscador siempre buscara con cualquier parámetro, 
    # siempre en cuando este estado = TRUE, inidica que está activo
    consulta = request.GET.get('q', '')
    lista_blogs = None
    list_blogs = []
    if consulta:
        lista_blogs = Blogs.objects.filter(
            Q(titulo__icontains=consulta) |
            Q(resumen__icontains=consulta) |
            Q(palabras_clave__icontains=consulta) |
            Q(categorias__nombre__icontains=consulta), estado=True).distinct()
    # else:
        # en caso si alguien entra directamente a /busquedas
        # lista_blogs = Curso.objects.all().order_by('-fecha_creacion')[:2]
    # paginandor
        for blog in lista_blogs:
           dict_blog = {}
           dict_blog['titulo'] = blog.titulo
           dict_blog['slug'] = blog.slug
           dict_blog['resumen'] = blog.resumen[0:250] + '...' if len(blog.resumen)>250 else blog.resumen
           dict_blog['contenido'] = blog.contenido
           dict_blog['categorias'] = blog.categorias
           dict_blog['portada'] = blog.portada
           dict_blog['fecha_publicacion'] = blog.fecha_publicacion
           dict_blog['autor'] = blog.autor
           dict_blog['vistas'] = blog.vistas
           dict_blog['palabras_clave'] = blog.palabras_clave
           dict_blog['estado'] = blog.estado
           dict_blog['es_pricipal'] = blog.es_pricipal
           dict_blog['posts_relacionados'] = blog.posts_relacionados
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

    categorias = Categoria.objects.all()

    return render(request, 'blog/buscador_blog.html',
                  {'blogs': blogs, 'categorias': categorias})


def buscador_categoria(request, slug):
    try:
        consulta = Blogs.objects.filter(
            categorias__slug=slug, estado=True)
        list_blogs = []
        for blog in consulta:
           dict_blog = {}
           dict_blog['titulo'] = blog.titulo
           dict_blog['slug'] = blog.slug
           dict_blog['resumen'] = blog.resumen[0:250] + '...' if len(blog.resumen)>250 else blog.resumen
           dict_blog['contenido'] = blog.contenido
           dict_blog['categorias'] = blog.categorias
           dict_blog['portada'] = blog.portada
           dict_blog['fecha_publicacion'] = blog.fecha_publicacion
           dict_blog['autor'] = blog.autor
           dict_blog['vistas'] = blog.vistas
           dict_blog['palabras_clave'] = blog.palabras_clave
           dict_blog['estado'] = blog.estado
           dict_blog['es_pricipal'] = blog.es_pricipal
           dict_blog['posts_relacionados'] = blog.posts_relacionados
           list_blogs.append(dict_blog)
        categorias = Categoria.objects.all()
        return render(request, 'blog/buscador_blog.html',
                      {'blogs': list_blogs, 'categorias': categorias})
    except Exception as e:
        raise 

class AcercaDe(TemplateView):
    template_name = 'blog/nosotros.html'

@csrf_exempt 
def contador_visitas(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            estado = False
            blog = get_object_or_404(Blogs, 
                estado=True, pk=request.POST.get('id'))
            blog.vistas +=1
            blog.save()
            estado = True
            response = JsonResponse({'estado': estado})
            return HttpResponse(response.content)            
        except Exception as e:
            print ("Error:", e)
            response = JsonResponse({'estado': estado, 'error': str(e)})
            return HttpResponse(response.content)            
    else:
        return redirect('/')

def tags(request, slug):
    try:
        consulta = Blogs.objects.filter(
            categorias__slug=slug)
        categorias = Categoria.objects.all()
        return render(request, 'blog/categorias.html',
                      {'blogs': consulta, 'slug': slug})
    except Exception as e:
        raise e