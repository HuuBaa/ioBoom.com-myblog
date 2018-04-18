from django.test import TestCase
from .models import Article,Tag,Comment,UserProfile
from django.contrib.auth.models import User
# Create your tests here.


class ArticleTest(TestCase):

    def test_article_create(self):
        u = User.objects.create(username='username')
        Article.objects.create(title='title', author=u, content='content')
        Article.objects.create(title='title2', author=u, content='content2')
        a_list=Article.objects.all()
        self.assertEqual(len(a_list),2)

    def test_article_tag(self):
        u = User.objects.create(username='username')
        t=Tag.objects.create(name='tag1')
        a=Article.objects.create(title='title', author=u, content='content')
        a.tags.add(t)
        self.assertEqual(a.tags.all()[0],t)

class TagTest(TestCase):
    def test_slug(self):
        t = Tag.objects.create(name='tag tag tag')
        self.assertEqual(t.slug,'tag-tag-tag')


