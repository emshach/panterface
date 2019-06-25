# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from . import views, friede_app
from .app import setup, routes
from .models import App
from .views import lookup
import traceback
import sys

app_name = 'friede'
urlpatterns = []

setup( friede_app, lookup, urlpatterns )

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
           chunk.append( url( r"^%s" % k, v[0], name=v[1] ))

    urlpatterns.append( url( r'^api/', include(( chunk, ns ))))

urlpatterns += [
    url( r'^api/?$', views.api_root, name='api-root' ),
    url( r'^.*',     views.index,    name='index'    ),
]
