#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name='article'

urlpatterns=[
    url(r'^all/$',views.all_articles,name='all_articles'),
    url(r'^(?P<article_id>[0-9]+)/$',views.article_detail,name='article_detail'),
]