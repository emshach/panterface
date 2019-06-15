# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .objects import Settings, Shells, getenv
from .models import *
from .util import split_dict
from django.db import transaction
from django.core.exceptions import FieldDoesNotExist
from importlib import import_module
from collections import deque
from packaging.version import parse as version_parse
import sys
import traceback
import pprint

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
registries = { v: k for k, v in types.items() }
auto_create = ( Icon, )

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
        ))

    except Exception as e:
        print >> sys.stderr, "got exception", type(e), e, 'in installapp'
        traceback.print_exc()
        return None, None

def installapp( name, module, title, description, icon='', rest=True,
                active=True, version=None, router=None, data=None ):
    try:
        path = name
        if not path.startswith( 'apps.' ):
            path = 'apps.' + path
        if not icon:
            icon = 'fontawesome.tablet-alt'
        if isinstance( icon, basestring ):
            icon, new = Icon.objects.get_or_create( path=icon )

        app, new = App.objects.get_or_create( path=path, defaults=dict(
            title=title,
            module=module,
            description=description,
            icon=icon,
            rest=rest,
            active=active,
            version='0.0.0',
        ))
        if data:
            upgradeapp( app, data, upto=version )
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

        if data:
            available = version_parse( '0.0.0' )
            for d in data:
                v = version_parse( d[0] )
                if v > available:
                    available = v

        app = App.objects.get( path=path )
        app.available = available
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
        print >> sys.stderr, "got exception", type(e), e, 'in installapp'
        traceback.print_exc()
        return None


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
    return (
        ( 'new.' + name,
          tuple (
              ( '_' + o , dict(
                  title="new {}".format(rs[o][ 'plural' ]).title(),
                  href="/new/{}".format(o),
                  data=dict( model="{}.{}".format( name, o ))),
                ( '#widgets', ( 'card', dict( path="new.{}_{}".format( name, o )))),
                ( '#screens', ( 'default', dict( path='form.single' ))))
              for o in objects )),
        ( 'delete.' + name,
          tuple (
              ( '_' + o, dict(
                  title="delete {}".format( rs[o][ 'plural' ]).title(),
                  href="/delete/{{{}.{}*}}".format( name, o )),
                ( '#widgets', ( 'card', dict( path="delete.{}_{}".format( name, o )))))
              for o in objects )),
        tuple (
            ( "{}.{}".format( action, name ),
              tuple (
                  ( '_' + o, dict(
                      title="{} {}".format( action, rs[o][ 'plural' ]).title(),
                      href="/{}/{{{}.{}*+}}".format( action, name, o )),
                    ( 'widgets', ( 'card', dict(
                        path="{}.{}_{}".format( action, name, o )))))
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
        ( 'add',
          ( 'to',
            tuple(
                ( "{0}_{1}.{0}_{2}".format( name, o, x ), dict(
                    title="add to {}: {}".format( o, x ).title(),
                    href="/add/to/{{{0}.{1}+}}/{{{0}.{2}+}}".format(
                        name, o, x )))
                for o in objects
                for x in rs[o][ 'has' ])),
          tuple(
              ( "{0}_{1}.{0}_{2}".format( name, o, x ), dict(
                  title="add {} to {}".format( o, x ).title(),
                  href="/add/{{{0}.{1}+}}/{{{0}.{2}+}}".format( name, o, x )))
              for o in objects
              for x in rs[o][ 'in' ])),
        ( 'remove',
          ( 'from',
            tuple(
                ( "{0}_{1}.{0}_{2}".format( name, o, x ), dict(
                    title="remove from {}: {}".format( o, x ).title(),
                    href="/remove/from/{{{0}.{1}+}}/{{{0}.{2}}}".format(
                        name, o, x )))
                for o in objects
                for x in rs[o][ 'has' ] )),
          tuple(
              ( "{0}_{1}.{0}_{2}".format( name, o, x ), dict(
                  title="remove {} from {}".format( o, x ).title(),
                  href="/remove/{{{}.{}+}}/{{{}.{}+}}".format(
                      name, o, name, x )))
              for o in objects
              for x in rs[o][ 'in' ])),
        tuple(
            ( "{}_{}".format( name, o ),
              ( 'edit', dict(
                  title="edit {}".format( rs[o][ 'plural' ]).title(),
                  href="{{{}.{}*""+}}/edit".format( name, o ))),
              tuple(
                  (( "add.{}_{}".format( name, x ),
                     dict(
                         title="add to {}: {}".format( o, x ).title(),
                         href="{{{0}.{1}+}}/add/{{{0}.{2}+}}".format( name, o, x ),
                         redirect_to="add.to.{0}_{1}.{0}_{2}".format( name, o, x ))),
                   ( "remove.{}_{}".format( name, x),
                     dict(
                         title="remove from {}: {}".format( o, x ).title(),
                         href="{{{0}.{1}+}}/remove/{{{0}.{2}}}".format( name, o, x ),
                         redirect_to="remove.from.{0}_{1}.{0}_{2}".format(
                             name, o, x ))))
                  for x in rs[o][ 'has' ]),
              tuple(
                  (( ".add.to.{}_{}".format( name, x ),
                     dict(
                         title="add {} to {}".format( o, x ).title(),
                         href="{{{0}.{1}+}}/add/to/{{{0}.{2}+}}".format( name, o, x ),
                         redirect_to="add.{0}_{1}.{0}_{2}".format( name, o, x ))),
                   ( ".remove.from.{}_{}".format( name, x ),
                     dict(
                         title="remove {} from {}".format( o, x ).title(),
                         href="{{{0}.{1}}}/remove/from/{{{0}.{2}}}".format( name, o, x ),
                         redirect_to="remove.{0}_{1}.{0}_{2}".format( name, o, x ))))
                  for x in rs[o][ 'in' ]))
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

@transaction.atomic
def upgradeapp( app, data, upto=None ):
    app_version = version_parse( app.version )
    max_version = None
    if upto:
        upto = version_parse( upto )

    def update_version():
        if max_version :
            app.version = max_version
            app.save()

    for tree in data:
        v = tree[0]
        tree = tree[1:]
        with transaction.atomic():
            max_version = v
            version = version_parse(v)
            if app_version >= version :
                continue
            if upto and version >= upto :
                break
            transaction.on_commit( update_version )
            stack = deque([ tree ])
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
                                    print 'bundle', path[0], '=',\
                                        pprint.pformat( bundle, indent=0, depth=3 )\
                                        .replace( "\n", ' ' )
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
                        stack.extend( tuple( (x, {}) for x in top[ ::-1 ]))
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
                        relations = {}
                        try:
                            app_field = model[0]._meta.get_field( 'app' )
                            if app_field.related_model is App:
                                search[ 'app' ] = app
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
                                try:
                                    if rm in registries:
                                        if not value.startswith( registries[ rm ]+'.' ):
                                            value = "{}.{}".format(
                                                registries[ rm ], value )
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
                            obj, new = model[0].objects.get_or_create(
                                defaults=updates, **search )
                            cr[0] = obj
                        updated = False
                        attached = False
                        att_new = False
                        if parent:
                            method = "add%s" % model[0]._meta.model_name
                            adder = getattr( parent, method, None )
                            if adder:
                                attached, att_new = adder( path[0], obj )
                        if attached and renamed:
                            attached.name = renamed
                            attached.save()
                        if not new:
                            for key, value in updates.items():
                                setattr( obj, key, value )
                                updated = True
                        for key, value in relations.items():
                            setattr( obj, key, value )
                        obj.save()
                        obj_name = getattr( obj, 'path', getattr( obj, 'name' ))
                        if obj_name.startswith( registry[0] + '.' ):
                            obj_name = obj_name[ (len( registry[0]) + 1): ]
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
