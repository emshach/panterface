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

def hack_reverse( alias, **kwargs ):
    namespace = kwargs[ 'request' ].resolver_match.namespace
    name = "%s:%s" % ( namespace, alias )
    return original_reverse( name, **kwargs )

relations.reverse = hack_reverse

name = 'friede'

registry_objects = 'container widget block screen shell theme slot app location'.split()
objects = registry_objects + 'link reference setting'.split()
relations = dict(
    container={
        'model'  : 'Container',
        'icon'   : 'fontawesome.box-open',
        'plural' : 'containers',
        'has'    : objects,
        'in'     : registry_objects
    },
    widget={
        'model'  : 'Widget',
        'icon'   : 'fontawesome.toggle-on',
        'plural' : 'widgets',
        'has'    : objects,
        'in'     : registry_objects
    },
    block={
        'model'  : 'Block',
        'icon'   : 'fontawesome.columns',
        'plural' : 'blocks',
        'has'    : objects,
        'in'     : registry_objects
    },
    screen={
        'model'  : 'Screen',
        'icon'   : 'fontawesome.desktop',
        'plural' : 'screens',
        'has'    : objects,
        'in'     : registry_objects
    },
    shell={
        'model'  : 'Shell',
        'icon'   : 'fontawesome.terminal',
        'plural' : 'shells',
        'has'    : objects,
        'in'     : registry_objects
    },
    theme={
        'model'  : 'Theme',
        'icon'   : 'fontawesome.image',
        'plural' : 'themes',
        'has'    : objects,
        'in'     : registry_objects
    },
    slot={
        'model'  : 'Slot',
        'icon'   : 'fontawesome.indent',
        'plural' : 'slots',
        'has'    : objects,
        'in'     : registry_objects
    },
    app={
        'model'  : 'App',
        'icon'   : 'fontawesome.mobile-alt',
        'plural' : 'apps',
        'has'    : objects,
        'in'     : registry_objects
    },
    location={
        'model'  : 'Location',
        'icon'   : 'fontawesome.location-arrow',
        'plural' : 'locations',
        'has'    : objects,
        'in'     : registry_objects
    },
    link={
        'model'  : 'Link',
        'icon'   : 'fontawesome.link',
        'plural' : 'links',
        'has'    : ''.split(),
        'in'     : registry_objects
    },
    reference={
        'model'  : 'Reference',
        'icon'   : 'fontawesome.external-link-alt',
        'plural' : 'references',
        'has'    : ''.split(),
        'in'     : registry_objects
    },
    setting={
        'model'  : 'Setting',
        'icon'   : 'fontawesome.cog',
        'plural' : 'settings',
        'has'    : ''.split(),
        'in'     : registry_objects
    },
)
actions = 'list view new edit report delete'.split()
router = routers.DefaultRouter()
routes = OrderedDict()

class NamedDefaultRouter( routers.DefaultRouter ):
    def __init__( self, name, *args, **kwargs ):
        self.root_view_name = "api-root-%s" % name
        super( NamedDefaultRouter, self ).__init__( *args, **kwargs )

def registrar( router, routes, module ):
    name = module.name
    myrouter = None
    try:
        myrouter = routes[ name ]
    except KeyError:
        myrouter = routes[ name ] = NamedDefaultRouter( name )
        view_routes[ name ] = "api-root-%s" % name
        # myrouter.root_view_name = "api-root-%s" % name

    def register( prefix, viewset ):
        myrouter.register( prefix , viewset )
    return register

def install():
    app, new = installapp(
        name='friede',
        icon='fontawesome.fire-alt',
        module='friede',
        title='Project Friede',
        description='''App platform with utilities for REST API setup and
    configurable shells and themes''',
        router=router,
        data=(
            ( '0.1.0',
              ( 'actions',
                ( 'list', dict(
                    icon='fontawesome.list',
                    title='List Object Data in Table Form',
                    description='''''')),
                ( 'view', dict(
                    icon='fontawesome.eye',
                    title='View Object(s) in Expanded Form',
                    description='''''')),
                ( 'new', dict(
                    icon='fontawesome.plus',
                    title='Make New Object(s)',
                    description='''''')),
                ( 'edit', dict(
                    icon='fontawesome.edit',
                    title='Edit Object(s)',
                    description='''''')),
                ( 'report', dict(
                    icon='fontawesome.file-upload',
                    title='View Generated Reports Based on Object Data',
                    description='''''')),
                ( 'delete', dict(
                    icon='fontawesome.trash',
                    title='Delete Object(s)',
                    description='''''')),
                ( 'add', dict(
                    icon='fontawesome.folder-plus',
                    title='Attach Object(s) to Applicable Related Object(s)',
                    description='''''')),
                ( 'remove', dict(
                    icon='fontawesome.folder-minus',
                    title='Remove Object(s) from Related Objects(s)',
                    description='''''')),
              ),
              ( 'widgets',
                ( 'help',
                  ( 'list', dict(
                      icon='fontawesome.list',
                      data=dict(
                          component='ActionHelpWidget',
                          action='list'
                      ))),
                  ( 'view', dict(
                      icon='fontawesome.eye',
                      data=dict(
                          component='ActionHelpWidget',
                          action='view'
                      ))),
                  ( 'new', dict(
                      icon='fontawesome.plus',
                      data=dict(
                          component='ActionHelpWidget',
                          action='new'
                      ))),
                  ( 'edit', dict(
                      icon='fontawesome.edit',
                      data=dict(
                          component='ActionHelpWidget',
                          action='edit'
                      ))),
                  ( 'report', dict(
                      icon='fontawesome.file-upload',
                      data=dict(
                          component='ActionHelpWidget',
                          action='report'
                      ))),
                  ( 'delete', dict(
                      icon='fontawesome.trash',
                      data=dict(
                          component='ActionHelpWidget',
                          action='delete'
                      ))),
                  ( 'add', dict(
                      icon='fontawesome.folder-plus',
                      data=dict(
                          component='ActionHelpWidget',
                          action='add'
                      ))),
                  ( 'remove', dict(
                      icon='fontawesome.folder-minus',
                      data=dict(
                          component='ActionHelpWidget',
                          action='remove'
                      )))),
                ( 'dashboard', dict (
                    icon='fontawesome.expand',
                    data=dict(
                        component='DashboardWidget'
                    ))),
                ( 'inline', dict(
                    icon='fontawesome.compress',
                    data=dict(
                        component='InlineWidget'
                    )
                )),
                ( 'adaptive', dict(
                    icon='fontawesome.plug',
                    data=dict(
                        component='AdaptiveWidget'
                    ))),
                ( 'view.from_model', dict(
                    icon='fontawesome.eye',
                    extends='adaptive',
                    data=dict(
                        component='ViewModelWidget'
                    ))),
                ( 'list.from_model', dict(
                    icon='fontawesome.list',
                    extends='adaptive',
                    data=dict(
                        component='ListModelWidget'
                    ))),
                ( 'new.from_model', dict(
                    icon='fontawesome.plus',
                    extends='adaptive',
                    data=dict(
                        component='NewModelWidget'
                    ))),
                ( 'edit.from_model', dict(
                    icon='fontawesome.edit',
                    extends='adaptive',
                    data=dict(
                        component='EditModelWidget'
                    ))),
                ( 'report.from_model', dict(
                    icon='fontawesome.file-upload',
                    extends='adaptive',
                    data=dict(
                        component='ReportModelWidget'
                    ))),
                ( 'delete.from_model', dict(
                    icon='fontawesome.trash',
                    extends='adaptive',
                    data=dict(
                        component='ModelWidget'
                    ))),
                ( 'add.from_model', dict(
                    icon='fontawesome.folder-plus',
                    extends='adaptive',
                    data=dict(
                        component='AddModelWidget'
                    ))),
                ( 'remove.from_model', dict(
                    icon='fontawesome.folder-minus',
                    extends='adaptive',
                    data=dict(
                        component='RemoveModelWidget'
                    ))),
                ( 'from relations', objects, relations ),),
              ( 'blocks',
                ( 'form',
                  ( 'group', dict(
                      icon='fontawesome.object-group',
                      data=dict(
                          component='FormGroup'
                      ))),
                  ( 'section', dict(
                      icon='fontawesome.paragraph',
                      data=dict(
                          component='FormSection'
                      ))),
                  ( 'calendar', dict(
                      icon='fontawesome.calendar-alt',
                      data=dict(
                          component='FormCalendar',
                      ))))),
              ( 'screens',
                ( 'form.single', dict(
                    icon='fontawesome.file-alt',
                    data=dict(
                        component='FormPage'
                    ))),
                ( 'list.from_model', dict(
                    icon='fontawesome.list',
                    data=dict(
                        component='ListModelPage'
                    ))),
              ),
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
              ( 'containers',
                ( 'links.menu', dict(
                    title='Menus',
                    description='Collection of all Menu Objects' ),
                  ( 'nav', dict(
                      title='Nav Menu',
                      description='Main Site Navigation Menu'
                  )))),
              ( 'links',
                ( 'menu.nav',
                  ( 'home', dict(
                      title='Home',
                      icon='fontawesome.home',
                      location='home' )),
                  ( '.apps', dict(
                      title='Apps',
                      icon='fontawesome.tablet-alt',
                      location='apps' )),
                  ( 'about', dict(
                      title='About Us',
                      icon='fontawesome.trademark',
                      location='about' )),
                  ( 'contact', dict(
                      title='Contact Us',
                      icon='fontawesome.phone',
                      location='contact' )))),
              ( 'themes',
                ( 'mayflower.acamar', dict(
                    templates='friede/mayflower/acamar',
                    title='Acamar Theme for Mayflower Shell',
                    description='''A soothing aquamarine theme''' ))),
              ( 'shells',
                ( 'mayflower', dict(
                    title='Mayflower Shell',
                    description='''Webapp shell based on Vue and UIKit

Uses an innovative hybrid web-app/command-line navigation system''',
                    templates='friede/mayflower' ),
                  ( 'themes', ( 'current', dict( path='mayflower.acamar' ))))),
            ), ))

def init( router, register, urlpatterns ):
    register( r'registries', views.RegistryViewSet  )
    register( r'containers', views.ContainerViewSet )
    register( r'widgets',    views.WidgetViewSet    )
    register( r'blocks',     views.BlockViewSet     )
    register( r'screens',    views.ScreenViewSet    )
    register( r'shells',     views.ShellViewSet     )
    register( r'themes',     views.ThemeViewSet     )
    register( r'slots',      views.SlotViewSet      )
    register( r'apps',       views.AppViewSet       )
    register( r'icons',      views.IconViewSet      )
    register( r'locations',  views.LocationViewSet  )
    register( r'links',      views.LinkViewSet      )
    register( r'references', views.ReferenceViewSet )
    register( r'settings',   views.SettingViewSet   )
    register( r'containerentries', views.ContainerEntryViewSet )
    register( r'widgetentries',    views.WidgetEntryViewSet    )
    register( r'blockentries',     views.BlockEntryViewSet     )
    register( r'screenentries',    views.ScreenEntryViewSet    )
    register( r'shellentries',     views.ShellEntryViewSet     )
    register( r'themeentries',     views.ThemeEntryViewSet     )
    register( r'slotentries',      views.SlotEntryViewSet      )
    register( r'appentries',       views.AppEntryViewSet       )
    register( r'locationentries',  views.LocationEntryViewSet  )
    register( r'iconentries',      views.IconEntryViewSet      )
    register( r'linkentries',      views.LinkEntryViewSet      )
    register( r'referenceentries', views.ReferenceEntryViewSet )
    register( r'settingentries',   views.SettingEntryViewSet   )
