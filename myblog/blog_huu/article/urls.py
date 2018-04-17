#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^all/$',views.list_all_articles,name='list_all_articles')
]