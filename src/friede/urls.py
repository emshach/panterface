# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include
from django.conf import settings
from . import views
from . import friede_app
from .friede_app import install, init, router, register, routes
from .models import App
from importlib import import_module

app_name = 'friede'
urlpatterns = []
try:
    install()
    init( router=router,
          register=register( router, routes, friede_app ),
          urlpatterns=urlpatterns )
    # apps = App.objects.filter( active=True ).exclude( name=app_name ).all()
    for app in settings.INSTALLED_APPS:
        if app == 'friede': continue
        name = app
        module = app
        if module:
            try:
                friede = import_module( "%s.friede_app" % module )
                friede.install()
                friede.init( router=router,
                             register=register(
                                 router=router, routes=routes, module=friede ),
                             urlpatterns=urlpatterns )
            except ImportError, AttributeError:
                continue        # TODO: maybe warn
except Exception:
    # pass                        # TODO: handle
    raise
urlpatterns.append( url( r'^api/', views.api_root, namespace='friede' ))
urlpatterns.extend([ url( r'^api/%s' % k, include( v.urls ), namespace='friede' )
                     for k, v in routes.items() ])
urlpatterns.append( url( r'^.*', views.index, name='index' ))
