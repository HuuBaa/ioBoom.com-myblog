#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    picture = forms.ImageField(label='更换头像', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    age = forms.IntegerField(label='年龄',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    birthday = forms.DateField(label='生日（格式1990/12/21）',required=False,widget=forms.DateInput(attrs={'class':'form-control'}))

    website = forms.URLField(label='个人网站',required=False,widget=forms.URLInput(attrs={'class':'form-control'}))
    hometown = forms.CharField(label='家乡',max_length=64, required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    introduction = forms.CharField(label='个人简介',max_length=128, required=False,widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:
        model=UserProfile
        exclude=('user',)
