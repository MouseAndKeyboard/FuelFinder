#!/usr/bin/env python3.9


from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
