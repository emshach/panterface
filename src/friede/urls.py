# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include
from django.conf import settings
from importlib import import_module
from . import views
from . import friede_app
from .friede_app import install, init, router, registrar, routes
from .models import App

app_name = 'friede'
urlpatterns = []
try:
    install()
    init( router=router,
          register=registrar( router, routes, friede_app ),
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
                             register=registrar(
                                 router=router, routes=routes, module=friede ),
                             urlpatterns=urlpatterns )
            except ImportError, AttributeError:
                continue        # TODO: maybe warn
except Exception:
    # pass                        # TODO: handle
    raise
urlpatterns += [ url( r"^api/%s/" % k, include( v.urls ))
                 for k, v in routes.items() ]
views.routes[ 'completions' ] = ( 'completions', [''] )
urlpatterns += [
    url( r'^api/complete/(?P<path>.*$)', views.api_complete, name='completions' ),
    url( r'^api/', views.api_root, name='api-root' ),
]
urlpatterns.append( url( r'^.*', views.index, name='index' ))
