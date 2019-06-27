# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from .app import setup, routes
from .views import api_root, index

app_name = 'friede'
urlpatterns = []

setup( urlpatterns )

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
    url( r'^api/?$', api_root, name='api-root' ),
    url( r'^.*',     index,    name='index'    ),
]
