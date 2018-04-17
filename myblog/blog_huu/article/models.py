from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Article(models.Model):
    title=models.CharField(max_length=32)
    post_time=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,related_name='articles')
    content=models.CharField(max_length=256*4)
    #Tag的实例可以使用t.articles查询相应tag下所有的article
    tags = models.ManyToManyField('Tag',blank=True,related_name='articles')
    likes=models.IntegerField(default=0)
    views=models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name=models.CharField(max_length=32,unique=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    content=models.CharField(max_length=128)
    post_time=models.DateTimeField(default=timezone.now)
    article=models.ForeignKey('Article',related_name='comments')



class UserProfile(models.Model):
    user=models.OneToOneField(User)
    age=models.IntegerField(blank=True)
    birthday=models.DateField(blank=True)
    picture=models.ImageField(blank=True,upload_to='profile_images')
    website=models.URLField(blank=True)
    hometown=models.CharField(max_length=64,blank=True)
    introduction=models.CharField(max_length=128,blank=True)

