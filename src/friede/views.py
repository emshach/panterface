# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .objects import getregistries, getenv
from .core import setup, setupshell, setuptheme, setupmenus
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import *
from .serializers import *
import json

### route views

def index( request ):
    env = getenv()
    # # get the shell
    menus = env.C.menus()
    if not menus:
        menus = setupmenus()
    menudata = json.dumps( menus.to_dict() )
    shell = env.H.current()
    if not shell:
        shell = setupshell( env )
    # and the selected theme for that shell
    theme = shell.T.current()
    if not theme:
        theme = setuptheme( shell )
    # TODO: DoesNotExistException
    context = dict(
        shell=shell,
        theme=theme,
        menus=menudata,
    )
    for registry in getregistries():
        context[ registry.name ] = registry
    return render( request, theme.home, context )

### rest api views



@api_view([ 'GET' ])
def api_root( request, format=None ):
    out = {}

    apps = App.objects.filter( active=True ).exclude( name=NAME ).all()
    for app in apps:
        name = app.name
        module = app.module
        rest = app.rest
        if module:
            try:
                urls = import_module( "%s.%s" % ( module, 'urls' ))
                
                if rest:
                    router = urls.router
                    match = r'^api/%s/' % name
                    urlpatterns.append(
                        url( match, include( router.urls, namespace='' )))
            except ImportError, AttributeError:
                continue
    return Response({
        'users': reverse( 'user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

class ContainerViewSet( viewsets.ModelViewSet ):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer


class WidgetViewSet( viewsets.ModelViewSet ):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer


class BlockViewSet( viewsets.ModelViewSet ):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer


class ScreenViewSet( viewsets.ModelViewSet ):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer


class ShellViewSet( viewsets.ModelViewSet ):
    queryset = Shell.objects.all()
    serializer_class = ShellSerializer


class ThemeViewSet( viewsets.ModelViewSet ):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer


class SlotViewSet( viewsets.ModelViewSet ):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer


class AppViewSet( viewsets.ModelViewSet ):
    queryset = App.objects.all()
    serializer_class = AppSerializer


class LocationViewSet( viewsets.ModelViewSet ):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LinkViewSet( viewsets.ModelViewSet ):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class ReferenceViewSet( viewsets.ModelViewSet ):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer


class SettingViewSet( viewsets.ModelViewSet ):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer

