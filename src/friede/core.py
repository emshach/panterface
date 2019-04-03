# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .objects import Settings, Shells, getenv, getregistries, getshell
from .models import *
from .util import split_dict
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from importlib import import_module
from collections import deque
from packaging import version.parse as version_parse

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
    menus = None
    try:
        menus = Contaianer.objects.get( path='links.menu' )
    except:
        menus = Container.objects.create( path='links.menu' )
        Link.objects.bulk_create([
            Link( path='links.menu.nav.home',
                  title='Home',
                  location=Location.objects.get( path='locations.home' )),
            Link( path='links.menu.nav.apps',
                  title='Apps',
                  location=Location.objects.get( path='locations.apps' )),
            Link( path='links.menu.nav.about',
                  title='About Us',
                  location=Location.objects.get( path='locations.about' )),
            Link( path='links.menu.nav.contact',
                  title='Contact Us',
                  location=Location.objects.get( path='locations.contact' ))
        ])
    env.addcontainer( 'menus', menus )
    return menus

def setupshell( env=None ):
    "make (and select) the default shell"
    if not env:
        env = getenv()
    shell = None
    try:
        shell = Shell.objects.get( path='shells.mayflower' )
    except:
        shell = Shell.objects.create(
            path='shells.mayflower',
            templates='friede/mayflower'
        )
    env.addshell( 'current', shell )
    setuptheme( shell )
    return shell

def setuptheme( shell=None ):
    "make (and select) the default theme for the current shell"
    if not shell:
        shell = Shells().mayflower.get()
    theme = None
    try:
        theme = Theme.objects.get( path='themes.acamar' )
    except ObjectDoesNotExist:
        theme = Theme.objects.create(
            name='themes.acamar',
            templates='friede/mayflower/acamar'
        )
    shell.addtheme( 'current', theme )
    return theme

@transaction.atomic
def installapp( name, module, title, description, icon='', rest=True,
                active=True, version=None, router=None, data=None ):
    from .models import App
    path = name
    if not path.startswith( 'apps.' ):
        path = 'apps.' + path
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
        updateapp( app, data, upto=version )
    return app, new

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
    settings=Setting
)
def mklocations( app, objects, relations ):
    actions = 'list view new edit report delete'.split()
    return (( 'list', tuple(
        (( relations[o][ 'plural' ], dict(
            title="list {}".format( relations[o][ 'plural' ]).title(),
            href="/list/{}".format( relations[o][ 'plural' ]))),
         ( o, dict(
             title="list {}".format( relations[o][ 'plural' ]).title(),
             redirect_to="list.{}".format( relations[o][ 'plural' ]))))
                    for o in objects )),
            tuple (
                ( action,
                  tuple (
                      ( y, dict( title="{} {}".format( action, y ).title(),
                                 href="/{}/{}".format( action, y )))
                          for w in (((o, o), ( o, relations[o][ 'plural' ]))
                                    for o in objects )
                          for x, y in w ))
                    for action in actions[1:] ),
            ( 'add',
              ( 'new',
                tuple(
                    ( o, dict(
                        title="add new {}".format(o).title(),
                        href="/add/new/{}".format(o) ))
                        for o in objects if relations[o][ 'in' ])),
              ( 'to',
                ( 'new',
                  tuple(
                      ( o, dict(
                          title="add new {}".format(o).title(),
                          href="/add/new/{}".format(o) ))
                          for o in objects if relations[o][ 'has' ])),
                tuple(
                    ( y, dict(
                        title="add to {}".format(y).title(),
                        href="/add/to/{}".format(y) ))
                        for w in (((o, o), ( o, relations[o][ 'plural' ]))
                                  for o in objects if relations[o][ 'has' ])
                        for x, y in w )),
              tuple(
                  ( y, dict(
                      title="add {}".format(y).title(),
                      href="/add/{}".format(y) ))
                      for w in (((o, o), ( o, relations[o][ 'plural' ]))
                                for o in objects if relations[o][ 'in' ])
                      for x, y in w )),
            ( 'remove',
              ( 'from',
                tuple(
                    ( y, dict(
                        title="remove from {}".format(y).title(),
                        href="/remove/from/{}".format(y) ))
                        for w in ((( o, o ), ( o, relations[o][ 'plural' ]))
                                  for o in objects if relations[o][ 'has' ])
                        for x, y in w )),
              tuple(
                  ( y, dict(
                      title="remove {}".format(y).title(),
                      href="/remove/{}".format(y) ))
                      for w in (((o, o), ( o, relations[o][ 'plural' ]))
                                for o in objects if relations[o][ 'in' ])
                      for x, y in w )),
            tuple(
                ( name, tuple(
                    ( action, "{}.{}".format( action, name ))
                        for action in actions ))
                    for pair in (( o, relations[o][ 'plural' ] ) for o in objects )
                    for name in pair ),
            tuple (
                ( y,
                  ( 'add',
                    dict(
                        title="add {}".format(y).title(),
                        redirect_to="add.{}".format(y)
                    )),
                  ( 'remove',
                    dict(
                        title="remove {}".format(y).title(),
                        redirect_to="remove.{}".format(y) )))
                    for w in (((o, o), ( o, relations[o][ 'plural' ]))
                              for o in objects if relations[o][ 'has' ])
                    for x, y in w ),
            tuple (
                (( "{}.add.to".format(y),
                   dict(
                       title="add to {}".format(y).title(),
                       redirect_to="add.to.{}".format(y) )),
                 ( "{}.remove.from".format(y),
                   dict(
                       title="remove from {}".format(y).title(),
                       redirect_to="remove.from.{}".format(y) )))
                    for w in (((o, o), ( o, relations[o][ 'plural' ]))
                              for o in objects if relations[o][ 'in' ])
                    for x, y in w ))

def getsimplefields( app, name, plural, model, exclude=( 'id' )):
    mod = None
    try:
        mod = import_module( app.module )
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
    return ( '.'+plural, dict(
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
            getsimplefields( app, name, relations[o][ 'plural' ],
                            relations[o][ 'model' ])
            for o in objects ))

shortcuts = dict(
    locations=mklocations,
    settings=mksettings
)

def updateapp( app, data, upto=None ):
    app_version = version_parse( app.version )
    max_version = None
    if upto:
        upto = version_parse( upto )

    def update_version():
        if max_version :
            app.version = max_version
            app.save()

    for v, tree, in data:
        with transaction.atomic():
            max_version = v
            version = version_parse(v)
            if app_version < version :
                continue
            if upto and version > upto :
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

            while stack:
                obj = cr[0]
                new = None
                top = stack.pop()
                if isinstance( top, tuple ):
                    if isinstance( top[0], basestring ):
                        tag = top[0]
                        if tag == 'from relations' :
                            try:
                                shortcuts[ registry[0] ]( app, *( top[1:] ))
                            except KeyError:
                                # TODO: maybe warn
                                pass
                        elif tag in types:
                            stack.append( popmodel )
                            model.appendleft( types[ tag ])
                            registry.appendleft( tag )
                            if path[0]:
                                "then this may add to the elemnts of the current object"
                            else:
                                obj = Container.objects.get( path=tag )
                                stack.append( popcr )
                                cr.appendleft( obj )
                        else:
                            if tag.startswith('.'):
                                tag = tag[1:]
                            stack.extend(( poppath, popcr ))
                            path.appendleft(( "{}.{}" if path[0] else "{}{}" ).format(
                                path[0], tag ))
                            cr.appendleft( None )
                    else:
                        # flatten tuples
                        stack.extend( top[ ::-1 ])
                elif isinstance( top, dict ):
                    search, updates = split_dict( top, 'name', 'path' )
                    for key, value in updates.items():
                        if not isinstance( value, basestring ):
                            continue
                        field = model[0]._meta.get_field( key )
                        if field.is_relation:
                            related = field.related_model.objects.get( path=value )
                            updates[ key ] = related
                    if not obj or type( obj ) is not model[0]:
                        obj, new = model[0].get_or_create( defaults=updates,
                                                           **search )
                    if not new:
                        for key, value in updates.items():
                            setattr( obj, key, value )
                        obj.save()
                elif callable( top ):
                    top()
