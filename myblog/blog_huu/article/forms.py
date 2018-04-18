#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):

    username = forms.CharField(max_length=12,required=True)
    age = forms.IntegerField(required=False)
    birthday = forms.DateField(required=False)
    picture = forms.ImageField(required=False)
    website = forms.URLField(required=False)
    hometown = forms.CharField(max_length=64, required=False)
    introduction = forms.CharField(max_length=128, required=False)

    class Meta:
        model=UserProfile
        exclude=('user',)
