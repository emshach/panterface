# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from importlib import import_module
from . import views
from . import friede_app
from .app import router, routes, apps
from .models import App
import traceback
import sys

app_name = 'friede'
urlpatterns = []
try:
    friede = friede_app.App()
    apps[ 'friede' ] = friede
    friede.install()
    friede.init( routes, views.routes, router, urlpatterns )
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
                    app.init( routes, views.routes, router, urlpatterns )
            except ( ImportError, AttributeError ) as e:
                msg = str(e)
                if 'No module named friede_app' not in msg:
                    print >> sys.stderr, 'got exception', type(e), e,\
                        "in friede.urls/%s" % module
                    traceback.print_exc()
                continue        # TODO: maybe warn
except Exception:
    # pass                        # TODO: handle
    raise

urlpatterns += [ u for x in tuple (
    ( url( r"^api/%s/" % k, include( v.urls )),
      url( r"^api/%s" % k, Redirect.as_view( url=reverse_lazy(
          "api-root-%s" % k, permanent=True )))) if hasattr( v, 'urls' )
    else ( url( r"^api/%s" % k, v[0], name=v[1] ), )
    for k, v in routes.items() )
                 for u in x ]
urlpatterns += [
    url( r'^api/?$', views.api_root, name='api-root' ),
    url( r'^.*',     views.index,    name='index'    ),
]
