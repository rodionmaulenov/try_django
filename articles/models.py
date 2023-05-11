from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.db.models import Q

from articles.utils import slugify_instance_title

User = settings.AUTH_USER_MODEL


class ArticleQuerySet(models.QuerySet):
    def search(self, query):
        if query is None or query == '':
            return self.none()
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.filter(lookups)


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, self._db)

    def search(self, query):
        return self.get_queryset().search(query)
    # def search(self, query):
    #     if query is None or query == '':
    #         return self.get_queryset().none()
    #     lookups = Q(title__icontains=query) | Q(content__icontains=query)
    #     return self.get_queryset().filter(lookups)


class Article(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now=False, auto_now_add=False,
                               null=True, blank=True)
    objects = ArticleManager()

    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'slug': self.slug})
    # def save(self, *args, **kwargs):
    # #     if self.slug is None:
    # #         self.slug = slugify(self.title)
    #     super().save(self, *args, **kwargs)


def pre_save_slug(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_title(instance, save=False)


pre_save.connect(pre_save_slug, sender=Article)


def post_save_slug(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)


post_save.connect(post_save_slug, sender=Article)
