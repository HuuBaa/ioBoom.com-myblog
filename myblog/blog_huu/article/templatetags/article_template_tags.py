#!/usr/bin/env python
#-*- coding: utf-8 -*-
from ..models import Article
from django import template

register=template.Library()

@register.inclusion_tag('article/_sidebar.html')
def get_sidebar_tag():
    return {}