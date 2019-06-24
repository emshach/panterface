# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include
from .views import login, logout, register

urlpatterns = [
    url( r'^register/', login, name='register' ),
    url( r'^login/', login, name='login' ),
    url( r'^logout/', login, name='logout' ),
]
