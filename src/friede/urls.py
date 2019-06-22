# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include
from django.conf import settings
from importlib import import_module
from . import views
from . import friede_app
from .app import router, registrar, routes, apps
from .models import App
import traceback
import sys

app_name = 'friede'
urlpatterns = []
try:
    friede = friede_app.App()
    apps['friede'] = friede
    friede.install()
    friede.init( router=router,
                 register=registrar( router, routes, friede ),
                 urlpatterns=urlpatterns )
    for app_name in settings.INSTALLED_APPS:
        if app_name == 'friede': continue
        name = app_name
        module = app_name
        if module:
            try:
                app = import_module( "%s.friede_app" % module )
                app = app.App()
                apps[ app.name ] = app
                if app.installed:
                    app.init( register=registrar( router=router, routes=routes, app=app ),
                              router=router,
                              urlpatterns=urlpatterns )
            except ( ImportError, AttributeError ) as e:
                msg = str( e )
                if 'No module named friede_app' not in msg:
                    print >> sys.stderr, 'got exception', type(e), e,\
                        "in friede.urls/%s" % module
                    traceback.print_exc()
                continue        # TODO: maybe warn
except Exception:
    # pass                        # TODO: handle
    raise

urlpatterns += [ url( r"^api/%s/" % k, include( v.urls ))
                 for k, v in routes.items() ]
views.routes[ 'ls' ] = ( 'ls', [''] )
views.routes[ 'models' ] = ( 'models', [''] )
views.routes[ 'path' ] = ( 'path', [''] )
urlpatterns += [
    url( r'^api/ls/(?P<path>.*$)', views.api_ls, name='ls' ),
    url( r'^api/models/(?P<models>.*$)', views.api_models, name='models' ),
    url( r'^api/path/(?P<path>.*$)', views.api_path, name='path' ),
    url( r'^api/', views.api_root, name='api-root' ),
]
urlpatterns.append( url( r'^.*', views.index, name='index' ))
