# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include
from . import views

app_name = 'intrepid'
urlpatterns = [
    url( r'^$', views.index, name='index' ),
]
