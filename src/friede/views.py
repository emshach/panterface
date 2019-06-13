# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import NOT_PROVIDED
from rest_framework import status, viewsets, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.exceptions import ValidationError
from rest_framework_serializer_extensions.views import SerializerExtensionsAPIViewMixin
from collections import OrderedDict
from importlib import import_module
from aries.auth import get_user
from .objects import getregistries, getenv, Locations
from .core import setup, setupshell, setuptheme, setupmenus
from .models import *
from .serializers import *
from .util import as_tree, form_field_mappings
import json
import re

### custom filters

class IdsFilter( filters.BaseFilterBackend ):
    """
    Filter for retrieving multiple objects by ID
    """
    def filter_queryset( self, request, queryset, view ):
        ids = request.query_params.get( 'ids' )
        if not ids:
            return queryset
        try:
            ids = [ int(x) for x in ids.split(',') if len(x) ]
        except Exception:
            raise ValidationError( "Only comma-separated list of IDs for ids filter" )
        if len( ids ):
            return queryset.filter( pk__in=ids )
        return queryset


class PathFilter( filters.BaseFilterBackend ):
    """
    Filter for retrieving multiple objects by ID
    """
    def filter_queryset( self, request, queryset, view ):
        path = request.query_params.get( 'path' )
        if path is None:
            return queryset
        rpath = request.path.split('/')
        while len( rpath ) and not rpath[-1]:
            rpath.pop()
        name = rpath[-1]
        if not path.startswith( name + '.' ):
            path = "{}.{}".format( name, path )
        return queryset.filter( path=path )


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
    models = {}
    apps = App.objects.filter( active=True ).all()
    for app in apps:
        try:
            app_models = ContentType.objects.filter( app_label=app.name ).all()
        except ContentType.DoesNotExist:
            continue
        mo = models[ app.name.encode( 'ascii', 'ignore' ) ] = {}
        for m in app_models:
            obj = m.model_class()
            model=m.model.encode( 'ascii', 'ignore' )
            singular = obj._meta.verbose_name.encode( 'ascii', 'ignore' )
            plural = obj._meta.verbose_name_plural.encode( 'ascii', 'ignore' )
            o = dict(
                model=model,
                singular=singular,
                plural=plural
            )
            mo[ model ] = o
            mo[ singular ] = o
            mo[ plural ] = o

    user = get_user( request )
    context = dict(
        shell=shell,
        theme=theme,
        menus=json.dumps( menus ),
        user=json.dumps( dict(
            uid=user.id,
            username=user.username,
            fname=user.first_name,
            lname=user.last_name,
            anonymous=user.anonymous,
        )),
        models=models
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

def _process_location( location ):
    out = {}
    for k, v in location.items():
        if k.endswith( '_entries' ):
            k0 = k[ 1:-8 ] + 's'
            o = out[k0] = {}
            for x in v:
                o[ x[ 'name' ]]=x[ 'entry' ]
        else:
            out[k] = v
    return out

def _process_locations( locations ):
    return [ _process_location(l) for l in locations ]

@api_view([ 'GET' ])
@permission_classes(( permissions.AllowAny, ))
def api_ls( request, path='', format=None ):
    ptree = path.split('/')
    rx = r'/?'
    for d in ptree:
        if d:
            rx = r"(?:{}/)?{}".format( rx, d )
    rx = r'^' + rx
    if path:
        rx = rx + r'(?:/|$)'
    candidates = Location.objects.filter( href__regex=rx ).all()
    completions = re.compile( r'%s([^/]*)(?:/|($))?' % rx )
    matches = set()
    slots = {}
    by_label = {}
    locations = []
    endpoint = False
    for candidate in candidates:
        if not candidate.href:
            continue
        m = completions.match( candidate.href )
        if m:
            g = m.group(1)
            if not g:
                endpoint = _process_location( LocationSerializer(
                    candidate, context=dict(
                        request= request,
                        detail=  True,
                        expand=  [ '_widget_entries', '_screen_entries' ])).data )
                continue
            m2 = re.match( r'{([\w.]+)(\*)?(\+)?}', g )
            if m2:
                slot = m2.group(1)
                if slot not in slots:
                    app, model = slot.split('.')
                    try:
                        obj = ContentType.objects.get( app_label=app, model=model )
                    except ContentType.DoesNotExist:
                        continue
                    obj = obj.model_class()
                    singular = obj._meta.verbose_name
                    plural = obj._meta.verbose_name_plural
                    slots[ slot ] = dict(
                        app=app,
                        model=model,
                        singular=singular,
                        plural=plural,
                        append='',
                        create=False,
                        multiple=False,
                        search=set(( app, model )))
                    if singular not in by_label:
                        by_label[ singular ] = []
                    by_label[ singular ].append( slots[ slot ])
                if m2.group(2):
                    slots[ slot ][ 'multiple' ] = True
                if m2.group(3):
                    slots[ slot ][ 'create' ] = True
                    slots[ slot ][ 'search' ].add( 'new' )
            else:
                matches.add(g)
                if m.group(2) is not None:
                    locations.append( candidate )
    for k, v in by_label.items():
        if len(v) > 1:
            for w in v:
                w[ 'append' ]= " ({})".format( w.app )
                w[ 'label' ]= ( w['plural' if w[ 'multiple'] else 'singular' ]
                               + w[ 'append' ]).title()
                w[ 'search' ] = list( w[ 'search' ])
        else:
            w = v[0]
            w[ 'label' ]= w['plural' if w[ 'multiple'] else 'singular' ].title()
            w[ 'search' ] = list( w[ 'search' ])

    expand = locations[ :1 ]
    rest = locations[ 1: ]
    expanded_serializer = LocationSerializer(
        expand, many=True, context=dict(
            request= request,
            detail=  True,
            expand=  [ '_widget_entries', '_screen_entries' ]))
    rest_serializer = LocationSerializer(
        rest, many=True, context={ 'request': request })
    return Response( dict(
        debug=dict(
            path=path,
            ptree=ptree,
            rx=rx
        ),
        endpoint=endpoint,
        base=rx,
        matches=tuple( matches ),
        slots=slots.values(),
        locations=_process_locations( expanded_serializer.data ) + rest_serializer.data
    ))

def _get_model( name ):
    app, model = name.split('.')
    try:
        obj = ContentType.objects.get( app_label=app, model=model )
    except ContentType.DoesNotExist:
        return None
    return obj.model_class()

@api_view([ 'GET' ])
@permission_classes(( permissions.AllowAny, ))
def api_models( request, models=None, format=None ):
    from friede.app import apps
    if not models:
        return Response({})
    while models.endswith('/'):
        models = models[:-1]
    models = [( m, True ) for m in models.split(',')[ ::-1 ]]
    out = {}
    have = set( request.query_params.getlist( 'have' ))
    while models:
        name, cont = models.pop()
        if not name or name in out or name in have: continue
        model = _get_model( name )
        if not model:
            return Response({ 'error': "found no model '%s'" % name },
                            status=status.HTTP_404_NOT_FOUND )

        meta = model._meta
        data = dict(
            name=meta.model_name,
            fullname=name,
            singular=meta.verbose_name,
            plural=meta.verbose_name_plural,
            fields=[],
        )
        out[ name ] = data
        app_obj = apps.get( meta.app_label )
        if app_obj is None:
            return Response({ 'error': "found no app '%s'" % meta.app_label },
                            status=status.HTTP_404_NOT_FOUND )
        sr = dict( app_obj.serializers ).get( meta.model_name )
        if sr is None:
            return Response({ 'error': "found no seralizer for '%s'" % name },
                            status=status.HTTP_404_NOT_FOUND )
        for f in meta.get_fields():
            if f.name not in sr.Meta.fields and (
                    not hasattr( sr.Meta, 'expandable_fields' )
                    or f.name not in sr.Meta.expandable_fields ):
                continue
            ftype0 = f.__class__.__name__
            ftype = ftype0
            if ftype in form_field_mappings:
                ftype = form_field_mappings[ ftype ]
                if not ftype: continue
            dflt = None
            if meta.model_name in app_obj.relations:
                dflt = app_obj.relations[ meta.model_name ].get( 'default' )
            field = dict(
                name=f.name,
                type=ftype,
                default=dflt,
            )
            if field.get( 'default' ) is None:
                try:
                    dflt = getattr( f, 'default' )
                    if dflt is dict:
                        dflt = ('f', 'Object' )
                    elif dflt in ( list, tuple ):
                        dflt = ( 'f', 'Array' )
                    elif dflt in ( int, float ):
                        dflt = ( 'f', 'Number' )
                    elif dflt in ( str, basestring ):
                        dflt = ( 'f', 'String' )
                    elif dflt is bool:
                        dflt = ( 'f', 'Boolean' )
                    elif callable( dflt ):
                        dflt = NOT_PROVIDED
                    if dflt is not NOT_PROVIDED:
                        field[ 'default' ] = dflt
                except AttributeError:
                    pass
            data[ 'fields' ].append( field )
            if getattr( f, 'related_model', None ):
                m = f.related_model
                related = "%s.%s" % ( m._meta.app_label, m._meta.model_name )
                field[ 'related' ] = related
                if not cont or related in out or related in have:
                    continue
                fm = app_obj.relations.get( meta.model_name )
                if fm is not None and fm.get( 'links' ) is not None\
                   and f.name in fm[ 'links' ]:
                    models.append(( related, False ))
                    if isinstance( fm[ 'links' ], dict )\
                       and fm[ 'links' ][ f.name ].get( 'via' ):
                        field[ 'link_field' ] = fm[ 'links' ][ f.name ][ 'via' ]
                elif 'Rel' not in ftype0:
                    models.append(( related, True ))
            # TODO: get field groups from settings

    return Response( dict( models=out ))

@api_view([ 'GET' ])
@permission_classes(( permissions.AllowAny, ))
def api_path( request, path=None, format=None ):
    from friede.app import apps
    nodes = tuple( x for x in path.split('/') if x )
    rx0 = '^'
    rx1 = ''
    endpoint = False
    lscontext = dict(
        request= request,
        detail=  True,
        expand=  [ '_widget_entries', '_screen_entries' ]
    )
    out = [
        dict(
            title='/',
            href='',
            location=_process_location( LocationSerializer(
                Location.objects.filter( href__regex=r'^/?$').first(),
                context=lscontext ).data )
        )]
    for n in nodes:
        endpoint = False
        node=dict( hash=n )
        if n[0] == '-':
            ndata = n[1:].split('+')
            odata = ndata[0].split('-')
            app = odata[0]
            reg = odata[1]
            ids = [ int(x) for x in odata[2:] ] # TODO: validationerror
            app_obj = apps.get( app )
            if app_obj is None:
                out.append(dict( error="no app object for '%s'" % app ))
                continue        # TODO: validationerror
            vs = dict( app_obj.routes ).get( reg )
            if vs is None:
                out.append(dict( error="no registry '%s' for '%s'" %( reg, app )))
                continue        # TODO: ''
            qs = vs.queryset
            model = qs.model
            meta = model._meta
            serializer = vs.serializer_class
            objects=qs.filter( pk__in=ids )
            data = serializer( objects, many=True, context={ 'request': request })
            node.update(
                app=app,
                model=meta.model_name,
                singular=meta.verbose_name,
                plural=meta.verbose_name_plural,
                objects=data.data,
                filter='+'.join( ndata[1:] ),
                filters= ndata[1:],
                href="{{{}\.{}\*?\+?}}".format( app, meta.model_name ),
                title='TBD'
            )
            rx0 = r"{}/{}".format( rx0, node[ 'href' ])
            rx1 = r"(?:{}/)?{}".format( rx1, node[ 'href' ])
            loc0 = Location.objects.filter( href__regex=rx0+r'/?$' )
            if len( loc0 ):
                node[ 'location' ] = _process_location(
                    LocationSerializer( loc0.first(), context=lscontext ).data )
                endpoint = True
            else:
                loc1 = Location.objects.filter( href__regex=rx1+r'/?$' )
                if len ( loc1 ):
                    node[ 'location' ] = _process_location(
                        LocationSerializer( loc1.first(), context=lscontext ).data )
                    endpoint = True
        elif n[0] == '@':
            users = n[1:].split('+')
        else:
            rx0 = r"{}/{}".format( rx0, n )
            rx1 = r"(?:{}/)?{}".format( rx1, n )
            loc0 = Location.objects.filter( href__regex=rx0+r'/?$' )
            if len( loc0 ):
                node['location'] = _process_location(
                    LocationSerializer( loc0.first(), context=lscontext ).data )
                endpoint = True
            else:
                loc1 = Location.objects.filter( href__regex=rx1+r'/?$' )
                if len ( loc1 ):
                    node[ 'location' ] = _process_location(
                        LocationSerializer( loc1.first(), context=lscontext ).data )
                    endpoint = True
            if 'href' not in node:
                node.update( href=n, title=n )
        out.append( node )
    return Response( dict( route=out, endpoint=endpoint ))

class SearchViewSet( viewsets.ModelViewSet ):
    filter_backends = ( IdsFilter, PathFilter, filters.SearchFilter, )
    search_fields = ( 'name', 'title', 'description' )


class RegistryViewSet( SerializerExtensionsAPIViewMixin, SearchViewSet ):
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


class LinkViewSet( SearchViewSet ):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class IconViewSet( SearchViewSet ):
    queryset = Icon.objects.all()
    serializer_class = IconSerializer


class ReferenceViewSet( SearchViewSet ):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer


class SettingViewSet( SearchViewSet ):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer


class ActionViewSet( SearchViewSet ):
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


