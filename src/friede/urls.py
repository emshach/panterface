# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from importlib import import_module
from . import views
from . import friede_app
from .app import router, routes, apps, namespace
from .models import App
from .views import lookup
import traceback
import sys

app_name = 'friede'
urlpatterns = []
try:
    friede = friede_app.App()
    apps[ 'friede' ] = friede
    friede.install()
    myroutes = namespace( routes, 'friede' )
    mylookup = namespace( lookup, 'friede' )
    friede.init( myroutes, mylookup, router, urlpatterns )
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
                    myroutes = namespace( routes, app.name )
                    mylookup = namespace( lookup, app.name )
                    app.init( routes, lookup, router, urlpatterns )
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

for ns, urls in routes.items():
    chunk = []
    for k, v in urls.items():
        if hasattr( v, 'urls' ):
            chunk += [
                url( r"^%s/" % k, include( v.urls )),
                url( r"^%s" % k, RedirectView.as_view(
                    url=reverse_lazy( "friede:{}:{}".format( ns, v.root_view_name )),
                    permanent=True ))]
        else:
           chunk.append( url( r"^%s" % k, v[0], name=v[2] ))

    urlpatterns.append(( chunk, ns ))

urlpatterns += [
    url( r'^api/?$', views.api_root, name='api-root' ),
    url( r'^.*',     views.index,    name='index'    ),
]
