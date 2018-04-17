from django.shortcuts import render
from django.http.response import HttpResponse
from .models import Comment,Article,Tag
# Create your views here.

def index(request):
    return HttpResponse('index')

def list_all_articles(request):
    all_articles=Article.objects.all()
    return HttpResponse(all_articles)