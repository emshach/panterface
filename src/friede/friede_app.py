# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import views, app
from .models import Setting

class App( app.App ):
    name        = 'friede'
    actions     = 'list view new edit report delete'.split()
    icon        = 'fontawesome.fire-alt'
    module      = 'friede'
    title       = 'Project Friede'
    description = 'App platform with utilities for REST API setup'\
        ' and configurable shells and themes.'

    registry_objects = '''container widget block screen shell theme slot app
                          location'''.split()
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
    data = (
        ( '0.1.0',
          ( '#actions',
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
          ( '#widgets',
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
          ( '#blocks',
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
          ( '#screens',
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
          ( '#locations',
            ( 'home',    dict( title='Home',       href='/'        )),
            ( '.apps',   dict( title='Apps',       href='/apps'    )),
            ( 'about',   dict( title='About Us',   href='/about'   )),
            ( 'contact', dict( title='Contact Us', href='/contact' )),
            ( 'from relations', objects, relations )),
          ( '#settings',
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
          ( '#containers',
            ( 'links.menu', dict(
                title='Menus',
                description='Collection of all Menu Objects' ),
              ( 'nav', dict(
                  title='Nav Menu',
                  description='Main Site Navigation Menu'
              )))),
          ( '#links',
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
          ( '#themes',
            ( 'mayflower.acamar', dict(
                templates='friede/mayflower/acamar',
                title='Acamar Theme for Mayflower Shell',
                description='''A soothing aquamarine theme''' ))),
          ( '#shells',
            ( 'mayflower', dict(
                title='Mayflower Shell',
                description='''Webapp shell based on Vue and UIKit

    Uses an innovative hybrid web-app/command-line navigation system''',
                templates='friede/mayflower' ),
              ( '#themes', ( 'current', dict( path='mayflower.acamar' ))))),
        ),
    )
    routes=(
        ( 'registries',       views.RegistryViewSet       ),
        ( 'containers',       views.ContainerViewSet      ),
        ( 'widgets',          views.WidgetViewSet         ),
        ( 'blocks',           views.BlockViewSet          ),
        ( 'screens',          views.ScreenViewSet         ),
        ( 'shells',           views.ShellViewSet          ),
        ( 'themes',           views.ThemeViewSet          ),
        ( 'slots',            views.SlotViewSet           ),
        ( 'apps',             views.AppViewSet            ),
        ( 'icons',            views.IconViewSet           ),
        ( 'locations',        views.LocationViewSet       ),
        ( 'links',            views.LinkViewSet           ),
        ( 'references',       views.ReferenceViewSet      ),
        ( 'settings',         views.SettingViewSet        ),
        ( 'containerentries', views.ContainerEntryViewSet ),
        ( 'widgetentries',    views.WidgetEntryViewSet    ),
        ( 'blockentries',     views.BlockEntryViewSet     ),
        ( 'screenentries',    views.ScreenEntryViewSet    ),
        ( 'shellentries',     views.ShellEntryViewSet     ),
        ( 'themeentries',     views.ThemeEntryViewSet     ),
        ( 'slotentries',      views.SlotEntryViewSet      ),
        ( 'appentries',       views.AppEntryViewSet       ),
        ( 'locationentries',  views.LocationEntryViewSet  ),
        ( 'iconentries',      views.IconEntryViewSet      ),
        ( 'linkentries',      views.LinkEntryViewSet      ),
        ( 'referenceentries', views.ReferenceEntryViewSet ),
        ( 'settingentries',   views.SettingEntryViewSet   ),
    )
