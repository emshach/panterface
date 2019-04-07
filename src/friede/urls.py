# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include
from django.conf import INSTALLED_APPS
from . import views
from . import friede
from .friede import install, init, router, register
from .models import App
from importlib import import_module

app_name = 'friede'
urlpatterns = []
try:
    install()
    init( router=router,
          register=register( router, friede ),
          urlpatterns=urlpatterns )
    # apps = App.objects.filter( active=True ).exclude( name=app_name ).all()
    for app in INSTALLED_APPS:
        if app == 'friede': continue
        name = app
        module = app
        if module:
            try:
                friede = import_module( "%s.friede" % module )
                friede.install()
                friede.init( router=router,
                             register=register( router=router, module=friede ),
                             urlpatterns=urlpatterns )
            except ImportError, AttributeError:
                continue        # TODO: maybe warn
except Exception:
    # pass                        # TODO: handle
    raise
urlpatterns.append( url( r'^api/', include( router.urls , namespace='friede' )))
urlpatterns.append( url( r'^.*', views.index, name='index' ))
