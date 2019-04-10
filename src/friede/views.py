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
from rest_framework_serializer_extensions.views import SerializerExtensionsAPIViewMixin
import json
import re

routes = {}

### route views

def index( request ):
    env = getenv()
    # # get the shell
    menus = env.C.menus()
    if not menus:
        menus = setupmenus()
    menus = menus.to_dict()
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
    path = re.sub( r'\s+', '/', path )
    path = re.sub( r'/+', '/', path )
    base = re.sub( '.*/', '', path )
    candidates = Location.objects.filter( href__startswith=path ).all()
    completions = re.compile( r'%s([^/]*)(/?$)?' % path )
    matches = set()
    locations = []
    for candidate in candidates:
        if not candidate.href:
            continue
        m = completions.match( candidate.href )
        if m:
            matches.add( base + m.group(1) )
            if m.group(2) is not None:
                locations.append( candidate )
    serializer = LocationSerializer(
        locations, many=True, context={ 'request': request })
    return Response({
        'base'      : base,
        'matches'   : tuple( matches ),
        'locations' : serializer.data
    })

class RegistryViewSet( SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet ):
    extensions_expand = set()
    extensions_expand_id_only = set()
    extensions_exclude = set()
    extensions_only = set()

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


class LocationViewSet( RegistryViewSet ):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    extensions_expand = set( LocationSerializer.Meta.expanded_fields.keys() )

    def get_serializer_context( self ):
        context = super(LocationViewSet, self).get_serializer_context()
        context.update( expand = LocationSerializer.Meta.expanded_fields.keys())
        return context

class LinkViewSet( viewsets.ModelViewSet ):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class IconViewSet( viewsets.ModelViewSet ):
    queryset = Icon.objects.all()
    serializer_class = IconSerializer


class ReferenceViewSet( viewsets.ModelViewSet ):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer


class SettingViewSet( viewsets.ModelViewSet ):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer


