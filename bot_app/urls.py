# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 12:57:57 2020

@author: Student
"""


from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]