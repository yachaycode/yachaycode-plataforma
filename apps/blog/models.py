from django.db import models
from django.template.defaultfilters import slugify
from apps.users.models import User
from martor.models import MartorField
# Create your models here.
class Category(models.Model):

    name = models.CharField(max_length=180, unique=True)
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = ('Categories')

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=350, unique=True)
    slug = models.SlugField(editable=False, null=True, max_length=250)
    summary = models.TextField(null=True, max_length=1800)
    content = MartorField()
    categories = models.ManyToManyField(Category)
    cover_image = models.ImageField(upload_to='cover-images-blog', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    number_views = models.PositiveIntegerField(default=0, blank=True, null=True)
    keywords = models.CharField(max_length=800, null=True, blank=True) 
    status = models.BooleanField(default=True)
    is_main_article = models.BooleanField(default=False)
    related_posts = models.ManyToManyField("self",
                                     verbose_name=("Related posts"), blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title or u''

# De momento no se esta usando
class VisitorCounter(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    counter = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '%s - %s' % (self.blog, self.counter) or u''