# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .objects import getregistries, getenv
from .core import setup, setupshell, setuptheme, setupmenus
from .models import *
from .serializers import *
from .util import as_tree
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
import json

routes = {}

### route views

def index( request ):
    env = getenv()
    # # get the shell
    menus = env.C.menus()
    if not menus:
        menus = setupmenus()
    menus = menus.to_dict()
    locations = as_tree( Location.objects.filter( active=True).all(), 'href', '/' )
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
        menus=json.dumps( menus ),
        locations=json.dumps( locations ),
    )
    for registry in getregistries():
        context[ registry.name ] = registry
    return render( request, theme.home, context )

### rest api views

def _normalize_lookup( lookup ):
    if isinstance( lookup, ( tuple, list )):
        lookup = list( lookup )
    else:
        lookup = [ lookup ]
    if len( lookup ) < 2:
        lookup.append([])
    if len( lookup ) < 3:
        lookup.append({})
    return lookup

@api_view([ 'GET' ])
@permission_classes(( permissions.AllowAny, ))
def api_root( request, format=None ):
    "Root view for Friede system REST API"
    out = {}
    for k, v in routes.items():
        v = _normalize_lookup(v)
        out[k] = reverse( "friede:%s" % v[0], args=v[1], kwargs=v[2],
                          request=request, format=None )
    return Response( out )

@api_view([ 'GET' ])
@permission_classes(( permissions.AllowAny, ))
def api_complete( request, path=None, format=None ):
    if not path:
        path = ''
    if not path.startswith('/'):
        path = '/'+path
    locations = Location.objects.filter( href__startswith=path ).all()
    serializer = LocationSerializer(
        locations, many=True, context={'request': request })
    return Response( serializer.data )

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

