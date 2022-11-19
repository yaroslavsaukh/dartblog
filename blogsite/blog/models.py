from django.db import models

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, verbose_name='Url', unique=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, verbose_name='Url', unique=True)
    author = models.CharField(max_length=150)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')
    views = models.IntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts')
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class Email(models.Model):
    email = models.EmailField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_at']
