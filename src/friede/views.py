# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .objects import getregistries, getenv, Locations
from .core import setup, setupshell, setuptheme, setupmenus
from .models import *
from .serializers import *
from .util import as_tree, form_field_mappings
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_serializer_extensions.views import SerializerExtensionsAPIViewMixin
from collections import OrderedDict
from importlib import import_module
import json
import re

routes = OrderedDict()

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
def api_complete( request, path='', format=None ):
    path = path.split('/')
    rx = r''
    for d in path:
        if d:
            rx = r"({}/)?{}".format( rx, d )
    rx = r'^' + rx
    base = path[-1]
    if not base:
        rx = rx + r'(/|$)'
    candidates = Location.objects.filter( href__regex=rx )
    candidates = candidates.order_by( 'name' ).all()
    expand = candidates[ :1 ]
    rest = candidates[ 1: ]
    completions = re.compile( r'%s([^/]*)(/|$)?' % path )
    matches = set()
    slots = {}
    locations = []
    for candidate in candidates:
        if not candidate.href:
            continue
        m = completions.match( candidate.href )
        if m:
            g = m.group(1)
            m2 = re.match( r'{(.*)}', g )
            if m2:
                slots[ m2.group(1)] = m2.group(1)
            else:
                matches.add( base + m.group(1) )
                if m.group(2) is not None:
                    locations.append( candidate )
    expanded_serializer = LocationSerializer(
        expand, many=True, context=dict(
            request= request,
            detail=  True,
            expand=  [ '_widget_entries' ]))
    rest_serializer = LocationSerializer(
        rest, many=True, context={ 'request': request })
    return Response( dict(
        debug=dict(
            path=path,
            rx=rx
        ),
        base=      base,
        matches=   tuple( matches ),
        slots=     slots,
        locations= expanded_serializer.data + rest_serializer.data
    ))

def _get_model( name ):
    model = name.split('.')
    app = ".".join( model[:-1] )
    model = model[-1]
    try:
        mod = import_module( "%s.%s" % ( app, 'models' ))
    except ImportError:
        return Response({ 'error': "found no models in '%s'" % app },
                        status=status.HTTP_404_NOT_FOUND )

    name = model
    model = getattr( mod, name, None )
    return model

@api_view([ 'GET' ])
@permission_classes(( permissions.AllowAny, ))
def api_models( request, models=None, format=None ):
    if not models:
        return Response({})
    models = models.split(',')[ ::-1 ]
    out = {}
    have = set( request.GET.getlist( 'have' ))
    while models:
        name = models.pop()
        if not name or name in out or name in have: continue
        model = _get_model( name )
        if not model:
            return Response({
                'error': "found no model '%s' in '%s.models'" % ( name, app ) },
                            status=status.HTTP_404_NOT_FOUND )

        meta = model._meta
        data = dict(
            name=meta.model_name,
            fields=[],
        )
        out[ name ] = data
        for f in meta.get_fields():
            ftype0 = f.__class__.__name__
            ftype = ftype0
            if ftype in form_field_mappings:
                ftype = form_field_mappings[ ftype ]
                if not ftype: continue
            field = dict( name=f.name, type=ftype )
            if getattr( f, 'related_model', None ):
                m = f.related_model
                related = "%s.%s" % ( m._meta.app_label, m.__name__)
                field[ 'related' ] = related
                if 'Rel' not in ftype0 and related not in out and related not in have:
                    models.append( related )
            # TODO: get field groups from settings
            data[ 'fields' ].append( field )

    return Response( dict( models=out ))

class RegistryViewSet( SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet ):
    queryset = Registry.objects.all()
    serializer_class = RegistrySerializer


class EntryViewSet( viewsets.ModelViewSet ):
    pass


class ContainerViewSet( RegistryViewSet ):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer


class WidgetViewSet( RegistryViewSet ):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer


class BlockViewSet( RegistryViewSet ):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer


class ScreenViewSet( RegistryViewSet ):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer


class ShellViewSet( RegistryViewSet ):
    queryset = Shell.objects.all()
    serializer_class = ShellSerializer


class ThemeViewSet( RegistryViewSet ):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer


class SlotViewSet( RegistryViewSet ):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer


class AppViewSet( RegistryViewSet ):
    queryset = App.objects.all()
    serializer_class = AppSerializer


class LocationViewSet( RegistryViewSet ):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


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


class ActionViewSet( viewsets.ModelViewSet ):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class ContainerEntryViewSet( EntryViewSet ):
    queryset = ContainerEntry.objects.all()
    serializer_class = ContainerEntrySerializer


class WidgetEntryViewSet( EntryViewSet ):
    queryset = WidgetEntry.objects.all()
    serializer_class = WidgetEntrySerializer


class BlockEntryViewSet( EntryViewSet ):
    queryset = BlockEntry.objects.all()
    serializer_class = BlockEntrySerializer


class ScreenEntryViewSet( EntryViewSet ):
    queryset = ScreenEntry.objects.all()
    serializer_class = ScreenEntrySerializer


class ShellEntryViewSet( EntryViewSet ):
    queryset = ShellEntry.objects.all()
    serializer_class = ShellEntrySerializer


class ThemeEntryViewSet( EntryViewSet ):
    queryset = ThemeEntry.objects.all()
    serializer_class = ThemeEntrySerializer


class SlotEntryViewSet( EntryViewSet ):
    queryset = SlotEntry.objects.all()
    serializer_class = SlotEntrySerializer


class AppEntryViewSet( EntryViewSet ):
    queryset = AppEntry.objects.all()
    serializer_class = AppEntrySerializer


class LocationEntryViewSet( EntryViewSet ):
    queryset = LocationEntry.objects.all()
    serializer_class = LocationEntrySerializer


class IconEntryViewSet( EntryViewSet ):
    queryset = IconEntry.objects.all()
    serializer_class = IconEntrySerializer


class LinkEntryViewSet( EntryViewSet ):
    queryset = LinkEntry.objects.all()
    serializer_class = LinkEntrySerializer


class ReferenceEntryViewSet( EntryViewSet ):
    queryset = ReferenceEntry.objects.all()
    serializer_class = ReferenceEntrySerializer


class SettingEntryViewSet( EntryViewSet ):
    queryset = SettingEntry.objects.all()
    serializer_class = SettingEntrySerializer


class ActionEntryViewSet( EntryViewSet ):
    queryset = ActionEntry.objects.all()
    serializer_class = ActionEntrySerializer


