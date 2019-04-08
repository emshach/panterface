# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import views
from .core import installapp
from .models import App, Setting
from .views import routes as view_routes
from importlib import import_module
from rest_framework import routers
from rest_framework import relations
from collections import OrderedDict

original_reverse = relations.reverse

def hack_reverse(alias, **kwargs):
    namespace = kwargs['request'].resolver_match.namespace
    name = "%s:%s" % (namespace, alias)
    return original_reverse(name, **kwargs)

relations.reverse = hack_reverse

name = 'friede'

objects = '''container widget block screen shell theme slot app location link
             reference setting'''.split()
relations = dict(
    container={
        'model'  : 'Container',
        'plural' : 'containers',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    widget={
        'model'  : 'Widget',
        'plural' : 'widgets',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    block={
        'model'  : 'Block',
        'plural' : 'blocks',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    screen={
        'model'  : 'Screen',
        'plural' : 'screens',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    shell={
        'model'  : 'Shell',
        'plural' : 'shells',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    theme={
        'model'  : 'Theme',
        'plural' : 'themes',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    slot={
        'model'  : 'Slot',
        'plural' : 'slots',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    app={
        'model'  : 'App',
        'plural' : 'apps',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    location={
        'model'  : 'Location',
        'plural' : 'locations',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    link={
        'model'  : 'Link',
        'plural' : 'links',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    reference={
        'model'  : 'Reference',
        'plural' : 'references',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    setting={
        'model'  : 'Setting',
        'plural' : 'settings',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
)
actions = 'list view new edit report delete'.split()
router = routers.DefaultRouter()
routes = OrderedDict()

class NamedDefaultRouter( routers.DefaultRouter ):
    def __init__( self, name, *args, **kwargs ):
        self.root_view_name = "api-root-%s" % name
        super( NamedDefaultRouter, self ).__init__( *args, **kwargs )

def register( router, routes, module ):
    name = module.name
    myrouter = None
    try:
        myrouter = routes[ name ]
    except KeyError:
        myrouter = routes[ name ] = NamedDefaultRouter( name )
        view_routes[ name ] = "api-root-%s" % name
        # myrouter.root_view_name = "api-root-%s" % name

    def _register( prefix, viewset ):
        myrouter.register( prefix , viewset )
    return _register

def install():
    app, new = installapp(
        name='friede',
        module='friede',
        title='Project Friede',
        description='''App platform with utilities for REST API setup and
    configurable shells and themes''',
        router=router,
        data=(
            ( '0.1.0',
              ( 'locations',
                ( 'home',    dict( title='Home',       href='/'        )),
                ( '.apps',   dict( title='Apps',       href='/apps'    )),
                ( 'about',   dict( title='About Us',   href='/about'   )),
                ( 'contact', dict( title='Contact Us', href='/contact' )),
                ( 'from relations', objects, relations )),
              ( 'settings',
                ( 'from relations', objects, relations ),
                ( 'sys', dict( title='System' ),
                  ( 'ui', dict( title='User Interface' ),
                    ( 'shell', dict(
                        type=Setting.Types.MODEL,
                        data=dict(
                            options='friede.Shell'
                        ))),
                    ( 'theme', dict(
                        type=Setting.Types.MODEL,
                        data=dict(
                            options='friede.Theme',
                            filter=( 'in', '$current_shell' )
                        )))))),
              ( 'links', ),
              ( 'widgets',
                ( 'dashboard', dict (
                    data=dict(
                        component='DashboardWidget'
                    ))),
                ( 'inline', dict(
                    data=dict(
                        component='InlineWidget'
                    )
                )),
                ( 'adaptive', dict(
                    data=dict(
                        component='AdaptiveWidget'
                    ))),
                ( 'view.from.model', dict(
                    extends='widgets.adaptive',
                    data=dict(
                        component='ViewModelWidget'
                    ))),
                ( 'new.from.model', dict(
                    extends='widgets.adaptive',
                    data=dict(
                        component='NewModelWidget'
                    ))),
                ( 'edit.from.model', dict(
                    extends='widgets.adaptive',
                    data=dict(
                        component='EditModelWidget'
                    ))),
                ( 'report.from.model', dict(
                    extends='widgets.adaptive',
                    data=dict(
                        component='ReportModelWidget'
                    ))),
                ( 'delete.from.model', dict(
                    extends='widgets.adaptive',
                    data=dict(
                        component='ReportModelWidget'
                    ))),
                tuple(
                    ( action,
                      tuple(( o, dict(
                          extends="widgets.{}.from.model".format( action ),
                          data=dict(
                              model="intrepid.{}".format( relations[o][ 'model' ]))
                      )) for o in objects ))
                  for action in actions[1:] )),
              ( 'blocks',
                ( 'form',
                  ( 'group', dict(
                      data=dict(
                          component='FormGroup'
                      ))),
                  ( 'section', dict(
                      data=dict(
                          component='FormSection'
                      ))),
                  ( 'calendar', dict(
                      data=dict(
                          component='FormCalendar',
                      ))))),
              ( 'screens',
                ( 'form.single', dict(
                    data=dict(
                        component='FormPage'
                    ))),
                ( 'list.from.model', dict(
                    data=dict(
                        component='ListModelPage'
                    ))),
              ),
            ), ))
def init( router, register, urlpatterns ):
    register( r'containers', views.ContainerViewSet )
    register( r'widgets',    views.WidgetViewSet    )
    register( r'blocks',     views.BlockViewSet     )
    register( r'screens',    views.ScreenViewSet    )
    register( r'shells',     views.ShellViewSet     )
    register( r'themes',     views.ThemeViewSet     )
    register( r'slots',      views.SlotViewSet      )
    register( r'apps',       views.AppViewSet       )
    register( r'locations',  views.LocationViewSet  )
    register( r'links',      views.LinkViewSet      )
    register( r'references', views.ReferenceViewSet )
    register( r'settings',   views.SettingViewSet   )

