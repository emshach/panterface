# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import pprint
import traceback
from collections import deque
from importlib import import_module
from .util import toversion
from django.core.exceptions import FieldDoesNotExist
from django.db import transaction, IntegrityError
from django.db.models.base import Model as BaseModel
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from .objects import Settings, Shells, getenv
from .models import *
from .util import split_dict

types = dict(
    containers=Container,
    widgets=Widget,
    blocks=Block,
    screens=Screen,
    shells=Shell,
    themes=Theme,
    slots=Slot,
    apps=App,
    locations=Location,
    links=Link,
    references=Reference,
    settings=Setting,
    icons=Icon,
    actions=Action,
)
ops = {}
deps = {}
registries = { v: k for k, v in types.items() }
auto_create = ( Icon, )

def _get_model( name, app=None ):
    app, model = app, name if app else name.split('.')
    try:
        obj = ContentType.objects.get( app_label=app, model=model )
    except ContentType.DoesNotExist:
        return None
    return obj.model_class()



def getdatum( model, **kw ):
    m = model
    if isinstance( model, basestring ):
        model = _get_model( model )
    if not isinstance( model, BaseModel ):
        raise Exception( "model '{}' not found".format(m) )
    return model.objects.get( **kw )

def setup():
    "make new settings"
    # settings = Settings()
    # shell_setting = settings.sys.ui.shell.get_or_create(
    #     type=Setting.Types.Choice,
    #     data=dict(
    #         model='Shell',
    #         registry__parent__name=''
    #     ))
    # maybe not yet
    env = getenv()
    shell = env.H.current
    if not shell:
        shell = Shells().mayflower.get()
        if not shell:
            shell = setupshell( env )

def setupmenus( env=None ):
    "make the default menu entries"
    if not env:
        env = getenv()
    menus, created = Container.objects.get_or_create(
        path='links.menu', defaults=dict(
            title='Menus',
            description='Collection of all Menu Objects' ))

    nav, navcreated = Container.objects.get_or_create(
        path='links.menu.nav', defaults=dict(
            title='Nav Menu',
            description='Main Site Navigation Menu'
        ))
    Link.objects.get_or_create(
        path='links.menu.nav.home', defaults=dict(
            title='Home',
            location=Location.objects.get( path='locations.home' )))
    Link.objects.get_or_create(
        path='links.menu.nav.apps', defaults=dict(
            title='Apps',
            location=Location.objects.get( path='locations.apps' )))
    Link.objects.get_or_create(
        path='links.menu.nav.about', defaults=dict(
            title='About Us',
            location=Location.objects.get( path='locations.about' )))
    Link.objects.get_or_create(
        path='links.menu.nav.contact', defaults=dict(
            title='Contact Us',
            location=Location.objects.get( path='locations.contact' )))

    if created:
        env.addcontainer( 'menus', menus )
    return menus

def setupshell( env=None ):
    "make (and select) the default shell"
    if not env:
        env = getenv()
    shell, new = Shell.objects.get_or_create(
        path='shells.mayflower', defaults=dict(
            path='shells.mayflower',
            templates='friede/mayflower'
    ))
    env.addshell( 'current', shell )
    if new or not shell.T.current():
        setuptheme( shell )
    return shell

def setuptheme( shell=None ):
    "make (and select) the default theme for the current shell"
    if not shell:
        shell = Shells().mayflower.get()
    theme, new = Theme.objects.get_or_create(
        path='themes.mayflower.acamar', defaults=dict(
            path='themes.mayflower.acamar',
            templates='friede/mayflower/acamar'
        ))
    shell.addtheme( 'current', theme )
    return theme

def installappheader( name, module, title, description, icon='', rest=True,
                      min_version='0.0.1',
                      required=False,
                      user_required=False,
                      user_installable=False,
                      auto_install=False,
                      router=None ):
    try:
        path = name
        if not path.startswith( 'apps.' ):
            path = 'apps.' + path
        if not icon:
            icon = 'fontawesome.tablet-alt'
        if isinstance( icon, basestring ):
            if not icon.startswith( 'icons.' ):
                icon = 'icons.' + icon
            icon, new = Icon.objects.get_or_create( path=icon )

        return App.objects.get_or_create( path=path, defaults=dict(
            title=title,
            module=module,
            description=description,
            icon=icon,
            rest=rest,
            active=False,
            version='0.0.0',
            min_version=min_version,
            required=required,
            user_required=user_required,
            user_installable=user_installable,
            auto_install=auto_install,
        ))

    except Exception as e:
        print >> sys.stderr, "got exception", type(e), e, 'in installapp'
        traceback.print_exc()
        return None, None

def installapp( name, module, title, description, icon='', rest=True,
                active=True, version=None, router=None, data=None, obj=None ):
    try:
        path = name
        if not path.startswith( 'apps.' ):
            path = 'apps.' + path
        if not icon:
            icon = 'fontawesome.tablet-alt'
        if isinstance( icon, basestring ):
            icon, new = Icon.objects.get_or_create( path=icon )

        app, new = ( obj.model, False ) if obj and obj.model \
            else App.objects.get_or_create( path=path, defaults=dict(
                    title=title,
                    module=module,
                    description=description,
                    icon=icon,
                    rest=rest,
                    active=active,
                    version='0.0.0',
            ))
        if data:
            if upgradeapp( app, data, upto=version ):
                app.installed = True
                app.save()
        else:
            app.installed = True
            app.save()
        return app, new
    except Exception as e:
        print >> sys.stderr, "got exception", type(e), e, 'in installapp'
        traceback.print_exc()
        return None, None

def updateapp( name, data=None, obj=None ):
    try:
        path = name
        if not path.startswith( 'apps.' ):
            path = 'apps.' + path

        app = obj.model if obj and obj.model else App.objects.get( path=path )
        if data:
            available = toversion( '0.0.0' )
            for d in data:
                v = toversion( d[0] )
                if v > available:
                    available = v
                if len(d) > 1:
                    addversionmeta( app, v, d[1] if isinstance( d[1], dict )
                                    else {}, obj )

        print path, v, 'available'

        app.available = str( available )
        if obj:
            app.min_version = obj.min_version
            app.required = obj.required
            app.user_required = obj.user_required
            app.user_installable = obj.user_installable
            app.auto_install = obj.auto_install
            app.auto_user_install = obj.auto_user_install
        app.save()
        return app

    except Exception as e:
        print >> sys.stderr, "got exception", type(e), e, 'in updateapp'
        traceback.print_exc()
        return None

def addversionmeta( app, version, meta, obj=None ):
    from .app import load
    appname = app.name
    appdeps = deps.get( appname )
    if not appdeps:
        appdeps = deps[ appname ] = {}
    versiondeps = appdeps.get( version )
    if versiondeps:
        if obj:
            obj.setversionmeta( version, 'depends', versiondeps )
        return versiondeps
    versiondeps = dict( meta.get( 'depends', {} ))
    if obj:
        obj.setversionmeta( version, 'depends', versiondeps )
    return versiondeps


def mkwidgets( app, objects, relations, actions=None ):
    name = app.name
    if not actions:
        actions = 'list view new edit report delete add remove'.split()
    return tuple(
        ( action,
          ( name,
            tuple(( '_' + o, dict(
                icon=relations[o].get( 'icon', None ),
                extends="{}.from_model".format( action ),
                data=dict(
                    model="{}.{}".format( name, o ))
            )) for o in objects )))
    for action in actions )


def mklocations( app, objects, relations, actions=None ):
    name = app.name
    rs = relations
    if not actions:
        actions = 'list view new edit report delete'.split()
        screens = dict(
            list='list.from_model',
            view='view.object',
            new='form.single',
            edit='form.single',
            report='report.from_model',
            delete='delete.from_model',
        )
    return (
        ( 'new.' + name,
          tuple (
              ( '_' + o , dict(
                  title="new {}".format(rs[o][ 'plural' ]).title(),
                  href="/new/{}".format(o),
                  data=dict( model="{}.{}".format( name, o ))),
                ( '#widgets', ( 'card', dict( path="new.{}_{}".format( name, o )))),
                ( '#screens', ( 'default', dict( path=screens[ 'new' ]))))
              for o in objects )),
        ( 'delete.' + name,
          tuple (
              ( '_' + o, dict(
                  title="delete {}".format( rs[o][ 'plural' ]).title(),
                  href="/delete/{{{}.{}*}}".format( name, o ),
                  data=dict( model="{}.{}".format( name, o ))),
                ( '#widgets', ( 'card', dict( path="delete.{}_{}".format( name, o )))))
              for o in objects )),
        tuple (
            ( "{}.{}".format( action, name ),
              tuple (
                  ( '_' + o, dict(
                      title="{} {}".format( action, rs[o][ 'plural' ]).title(),
                      href="/{}/{{{}.{}*+}}".format( action, name, o ),
                      data=dict( model="{}.{}".format( name, o ))),
                    ( '#widgets', ( 'card', dict(
                        path="{}.{}_{}".format( action, name, o )))),
                    ( '#screens', ( 'default', dict( path=screens[ action ]))))
                  for o in objects ))
            for action in actions if action not in ( 'new', 'delete' )),
        ( '.' + name,
          tuple (
              ( '_' + o, dict(
                  title="view {}".format(o).title(),
                  href="{{{0}.{1}+}}".format( name, o ),
                  redirect_to="view.{}_{}".format( name, o )))
              for o in objects ),
          tuple (
              ( '.' + rs[o][ 'plural' ],
                dict( title="list {}".format( rs[o][ 'plural' ]).title(),
                      href="/{}/{}".format( name, rs[o][ 'plural' ] ),
                      redirect_to="list.{}_{}".format( name, o )))
              for o in objects )),
        tuple(
            ( "{}_{}.edit".format( name, o ), dict(
                title="edit {}".format( rs[o][ 'plural' ]).title(),
                href="{{{}.{}*""+}}/edit".format( name, o ),
                data=dict( model="{}.{}".format( name, o ))),
              ( '#screens', ( 'default', dict( path=screens[ 'edit' ]))))
            for o in objects ))

def getsimplefields( app, name, plural, model, exclude=( 'id' )):
    mod = None
    try:
        mod = import_module( "%s.%s" % ( app.module, 'models' ))
    except ImportError:
        return ()

    model = getattr( mod, model, None )
    if not model:
        return ()
    fields = tuple( f.name for f in model._meta.get_fields()
                    if ( f.model == model and not f.auto_created
                         and f.name not in exclude and (
                             not f.is_relation
                             or f.one_to_one
                             or ( f.many_to_one and f.related_model ))))
    return ( '.' + plural, dict(
        type=Setting.Types.MULTIPLECHOICE,
        data=dict(
            options=fields,
            values=fields )))

def mksettings( app, objects, relations ):
    path = app.path
    if path.startswith( 'apps.' ):
        path = path[5:]
    return (
        "views.list.fields.{}".format( path ),
        tuple(
            getsimplefields( app, o, relations[o][ 'plural' ],
                             relations[o][ 'model' ])
            for o in objects ))

shortcuts = dict(
    widgets=mkwidgets,
    locations=mklocations,
    settings=mksettings,
)

def _data_norm( app, mod, data, memo ):
    if not isinstance( data, ( tuple, list )):
        data = () if data is None else data,
    if isinstance( mod, basestring ):
        if mod == '.':
            mod = memo[ 'model' ]
        else:
            mod = _get_model( mod ) if '.' in mod \
                else _get_model( mod, app )
    return mod, data, dict( memo, model=mod )

def _data_norm_val( app, data, memo ):
    if isinstance( data, tuple ):
        if isinstance( data[0], basestring ):
            if data[0] == '.':
                data = ( '#get', ) + data
            if data[0].startswith('#'):
                tag = data[0][ 1: ]
                op = ops.get( tag )
                if op:
                    return op( app, data[1], data[ 2: ], memo )
    return data

def data_get( app, mod, data, memo={} ):
    model, _, _ = _data_norm( app, mod, data, memo )
    return model.objects.get( **( data[0] ))

def data_filter( app, mod, data, memo={} ):
    model, _, _ = _data_norm( app, mod, data, memo )
    return model.objects.filter( **data ).all()

def data_create( app, mod, data, memo={} ):
    model, data, memo = _data_norm( app, mod, data, memo )
    obj = None
    for search in data:
        d = {}
        if isinstance( search, tuple ):
            search, d = search
            d = { k : _data_norm_val( app, v, memo )
                  for k, v in d.items() }
        search = { k : _data_norm_val( app, v, memo )
                   for k, v in search.items() }
        try:
            obj = model.objects.get( **search )
        except model.DoesNotExist:
            obj = model.objects.create( **dict( search, **d ))
            print "Created {}: {}".format( model._meta.verbose_name, obj )
    return obj

def data_update( app, mod, data, memo={} ):
    model, data, memo = _data_norm( app, mod, data, memo )
    obj = []
    for search in data:
        d = {}
        if not isinstance( search, tuple ):
            continue
        search, d = search
        d = { k : _data_norm_val( app, v, memo )
              for k, v in d.items() }
        search = { k : _data_norm_val( app, v, memo )
                   for k, v in search.items() }
        obj = model.objects.filter( **search )
        if len( obj ):
            obj.update( **d )
            for o in obj:
                o.save()
    return obj[0] if len( obj ) == 1 else obj

def data_ensure( app, mod, data, memo={} ):
    model, data, memo = _data_norm( app, mod, data, memo )
    obj = None
    for search in data:
        d = {}
        if isinstance( search, tuple ):
            search, d = search
            d = { k : _data_norm_val( app, v, memo )
                  for k, v in d.items() }
        search = { k : _data_norm_val( app, v, memo )
                   for k, v in search.items() }
        if d:
            search[ 'defaults' ] = d
        obj, new = model.objects.update_or_create( **search )
        print "{} {}: {}".format( 'Created' if new else 'Updated',
                               model._meta.verbose_name, obj )
    return obj

def data_default( app, mod, data, memo={} ):
    model, data, memo = _data_norm( app, mod, data, memo )
    obj = []
    for search in data:
        d = {}
        if not isinstance( search, tuple ):
            continue
        search, d = search
        d = { k : _data_norm_val( app, v, memo )
              for k, v in d.items() }
        search = { k : _data_norm_val( app, v, memo )
                   for k, v in search.items() }
        obj = model.objects.filter( **search )
        if d and len( obj ):
            for o in obj:
                updated = False
                for k, v in d.items():
                    if getattr( o, k ) is None:
                        updated = True
                        setattr( o, k, v )
                if updated:
                    print "Updated %s" % o
                    o.save()
    return obj[0] if len( obj ) == 1 else obj

def data_delete( app, mod, data, memo={} ):
    model, data, memo = _data_norm( app, mod, data, memo )
    obj = []
    for search in data:
        search = { k : _data_norm_val( app, v, memo )
                   for k, v in search.items() }
        obj = model.objects.filter( **search )
        if len( obj ):
            obj.remove()
            for o in obj:
                print "Removed %s" % o
    return obj[0] if len( obj ) == 1 else obj

def data_link( app, mod, data, memo={} ):
    model, data, memo = _data_norm( app, mod, data, memo )

def data_unlink( app, mod, data, memo={} ):
    model, data, memo = _data_norm( app, mod, data, memo )

ops.update(
    get=data_get,
    filter=data_filter,
    data=lambda app, mod, data, memo={} : data,
    create=data_create,
    update=data_update,
    ensure=data_ensure,
    default=data_default,
    delete=data_delete,
    link=data_link,
    unlink=data_unlink,
)


def upgradeapp( app, data, upto=None ):
    app_version = toversion( app.version )
    max_version = None
    min_version = toversion( app.min_version )
    upgraded = dict( val=False )
    if upto:
        upto = toversion( upto )

    def update_version():
        if max_version :
            print "now at version", max_version
            app.version = max_version
            app.save()
            upgraded[ 'val' ] = True

    for tree in data:
        v = tree[0]
        max_version = v
        version = toversion(v)
        if app_version >= version :
            continue
        if upto:
            if version > upto :
                break
        elif min_version and app_version >= min_version:
            break
        with transaction.atomic():
            transaction.on_commit( update_version )
            stack = deque([ tree[2:]
                            if len (tree) > 1 and isinstance( tree[1], dict )
                            else tree[1:] ])
            path = deque([''])
            model = deque([ Container ])
            registry = deque([ 'containers' ])
            cr = deque([ None ])

            def popstack():
                stack.pop()

            def poppath():
                path.popleft()

            def popmodel():
                model.popleft()
                registry.popleft()

            def popcr():
                cr.popleft()

            try:
                while stack:
                    obj = cr[0]
                    new = None
                    top = stack.pop()
                    # print 'top=', top
                    if isinstance( top, tuple ):
                        if not len( top ):
                            continue
                        if isinstance( top[0], basestring ):
                            tag = top[0]
                            inst = False
                            if tag[0] == '#':
                                tag = tag[1:]
                                inst = True
                            if tag == 'from relations' :
                                try:
                                    bundle = shortcuts[ registry[0] ]( app, *( top[1:] ))
                                    # print 'bundle', path[0], '=',\
                                    #     pprint.pformat( bundle, indent=0, depth=3 )\
                                    #     .replace( "\n", ' ' )
                                    stack.append( bundle )
                                except KeyError as e:
                                    print >> sys.stderr, e
                                    pass
                            elif inst and tag in types:
                                stack.append( popmodel )
                                model.appendleft( types[ tag ])
                                registry.appendleft( tag )
                                if path[0]:
                                    "this may add to the elemnts of the current object"
                                    if not obj:
                                        obj, new = Container.objects.get_or_create(
                                            path=path[0] )
                                        cr[0] = obj
                                    stack.append( poppath )
                                    path.appendleft('')
                                else:
                                    obj, new = Container.objects.get_or_create(
                                        path=tag )
                                    stack.extend(( poppath, popcr ))
                                    cr.appendleft( obj )
                                    path.appendleft( tag )
                                stack.extend( top[1:][ ::-1 ])
                            elif inst and tag in ops:
                                op = ops[ tag ]
                                op( app.name, top[1], top[ 2: ])
                            else:
                                if tag.startswith('.'):
                                    tag = tag[1:]
                                stack.extend(( poppath, popcr ))
                                path.appendleft(
                                    ( "{}.{}" if path[0] and not tag.startswith('_')
                                      else "{}{}" ).format( path[0], tag ))
                                cr.appendleft( None )
                                stack.extend( top[1:][ ::-1 ])
                        else:
                            # flatten tuples
                            stack.extend( top[ ::-1 ])
                    elif isinstance( top, list ):
                        stack.extend( tuple(( x, {} ) for x in top[ ::-1 ]))
                    elif isinstance( top, dict ):
                        parent = None
                        if top.get( 'path', None ):
                            if not top[ 'path' ].startswith( registry[0] + '.' ):
                                top[ 'path' ] = "{}.{}".format(
                                    registry[0], top[ 'path' ])
                            for c in cr:
                                if c and type(c) is not Container:
                                    parent = c
                                    break
                        else:
                            top[ 'path' ] = path[0]
                        search, updates = split_dict( top, 'name', 'path' )
                        entry_updates = updates.pop( 'entry', {} )
                        append = updates.pop( 'APPEND', {} )
                        prepend = updates.pop( 'PREPEND', {} )
                        delete = updates.pop( 'DELETE', {} )
                        updated = False
                        attached = False
                        att_new = False
                        relations = {}
                        try:    # BWAHAHAHAHA!
                            app_field = model[0]._meta.get_field( 'app' )
                            if app_field.related_model is App:
                                if model[0] in ( Location, ):
                                    search[ 'app' ] = app
                                else:
                                    updates[ 'app' ] = app
                        except FieldDoesNotExist:
                            pass
                        renamed = False
                        if 'rename' in updates:
                            renamed = updates[ 'rename' ];
                            del updates[ 'rename' ]
                        for key, value in updates.items():
                            if not isinstance( value, basestring ):
                                continue
                            field = model[0]._meta.get_field( key )
                            if field.is_relation:
                                rm = field.related_model
                                updates.pop( key, None )
                                if rm in registries:
                                    if not value.startswith( registries[ rm ]+'.' ):
                                        value = "{}.{}".format(
                                            registries[ rm ], value )
                                try:
                                    related = rm.objects.get( path=value )
                                except rm.DoesNotExist:
                                    if rm in auto_create:
                                        related = rm.objects.create( path=value )
                                    else:
                                        print >> sys.stderr, "got no", rm, 'path', value
                                        raise
                                relations[ key ] = related
                                # TODO; account for multiple ordinality
                        if not obj or type( obj ) is not model[0]:
                            obj, new = model[0].objects.update_or_create(
                                defaults=updates, **search )
                            cr[0] = obj
                        for key, value in relations.items():
                            setattr( obj, key, value )
                        if not new and ( updates or relations ):
                            updated = True
                        if relations:
                            obj.save()
                        for key, value in append:
                            pass # TODO: implement
                        for key, value in prepend:
                            pass # TODO: implement
                        for key, value in delete:
                            pass # TODO: implement
                        if append or prepend or delete:
                            updated = True
                            obj.save()
                        obj_name = getattr( obj, 'path', getattr( obj, 'name' ))
                        if obj_name.startswith( registry[0] + '.' ):
                            obj_name = obj_name[ (len( registry[0]) + 1): ]

                        if parent:
                            method = "add%s" % model[0]._meta.model_name
                            adder = getattr( parent, method, None )
                            if adder:
                                if entry_updates:
                                    updates = entry_updates
                                    append = updates.pop( 'APPEND', {} )
                                    prepend = updates.pop( 'PREPEND', {} )
                                    delete = updates.pop( 'DELETE', {} )
                                else:
                                    updates = {}

                                attached, att_new = adder( path[0], obj, updates )
                                if attached:
                                    name = attached.name
                                    for key, value in append:
                                        pass # TODO: implement
                                    for key, value in prepend:
                                        pass # TODO: implement
                                    for key, value in delete:
                                        pass # TODO: implement
                                    if renamed:
                                        attached.name = renamed
                                    if append or prepend or delete or renamed:
                                        try:
                                            attached.save()
                                        except IntegrityError:
                                            print >> sys.stderr,\
                                                "Update failed, could not rename\
 '{}' to '{}': there is already an entry with that name".format( name, renamed )

                        if new:
                            print 'created', app.name, obj._meta.object_name, \
                                obj_name
                        elif updated:
                            print 'updated', app.name, obj._meta.object_name, \
                                obj_name
                        if attached:
                            if renamed:
                                print 'renamed', getattr( parent, 'path',
                                                          getattr( parent, 'name' )),\
                                    model[0]._meta.model_name, 'entry'
                                path[0], 'to', renamed
                            elif att_new:
                                print 'attached', obj._meta.object_name, obj_name, 'to',\
                                    getattr( parent, 'path', getattr( parent, 'name' ))
                    elif callable( top ):
                        top()
            except Exception as e:
                print >> sys.stderr, "got exception", type(e), e
                raise
        app_version = version
    return upgraded[ 'val' ]
