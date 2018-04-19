from django.db import models

from django.utils import timezone
from django.template.defaultfilters import slugify
from django.conf import settings
# Create your models here.

class Article(models.Model):
    title=models.CharField(max_length=32)
    post_time=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='articles')
    content=models.TextField(max_length=256*4)
    #Tag的实例可以使用t.articles查询相应tag下所有的article
    tags = models.ManyToManyField('Tag',blank=True,related_name='articles')
    likes=models.IntegerField(default=0)
    views=models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name=models.CharField(max_length=32,unique=True)
    slug=models.SlugField(unique=True)

    def save(self, *args, **kw):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kw)

    def __str__(self):
        return self.name

class Comment(models.Model):
    author=models.ForeignKey(settings.AUTH_USER_MODEL)
    content=models.TextField(max_length=128)
    post_time=models.DateTimeField(default=timezone.now)
    article=models.ForeignKey('Article',related_name='comments')


class UserProfile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL)
    age=models.IntegerField(blank=True,null=True)
    birthday=models.DateField(blank=True,null=True)
    picture=models.ImageField(blank=True,upload_to='profile_images',null=True)
    website=models.URLField(blank=True,null=True)
    hometown=models.CharField(max_length=64,blank=True,null=True)
    introduction=models.CharField(max_length=128,blank=True,null=True)

