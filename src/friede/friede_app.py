# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import views, serializers, app
from .app import action
from .models import Setting, App as AppModel, UserApp
from packaging.version import parse as version_parse


_links = '''_container_entries _widget_entries _block_entries _screen_entries
               _shell_entries _theme_entries _slot_entries _app_entries
               _location_entries _icon_entries _link_entries _reference_entries
               _setting_entries _action_entries'''.split()

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

    links = { x: dict( via='entry' ) for x in _links }

    min_version = '0.2.5'
    required = True
    user_required = True

    relations = dict(
        container={
            'model'  : 'Container',
            'icon'   : 'fontawesome.box-open',
            'plural' : 'containers',
            'has'    : objects,
            'in'     : registry_objects,
            'links'  : links,
        },
        widget={
            'model'  : 'Widget',
            'icon'   : 'fontawesome.toggle-on',
            'plural' : 'widgets',
            'has'    : objects,
            'in'     : registry_objects,
            'links'  : links,
        },
        block={
            'model'  : 'Block',
            'icon'   : 'fontawesome.columns',
            'plural' : 'blocks',
            'has'    : objects,
            'in'     : registry_objects,
            'links'  : links,
        },
        screen={
            'model'  : 'Screen',
            'icon'   : 'fontawesome.desktop',
            'plural' : 'screens',
            'has'    : objects,
            'in'     : registry_objects,
            'links'  : links,
        },
        shell={
            'model'  : 'Shell',
            'icon'   : 'fontawesome.terminal',
            'plural' : 'shells',
            'has'    : objects,
            'in'     : registry_objects,
            'links'  : links,
        },
        theme={
            'model'  : 'Theme',
            'icon'   : 'fontawesome.image',
            'plural' : 'themes',
            'has'    : objects,
            'in'     : registry_objects,
            'links'  : links,
        },
        slot={
            'model'  : 'Slot',
            'icon'   : 'fontawesome.indent',
            'plural' : 'slots',
            'has'    : objects,
            'in'     : registry_objects,
            'links'  : links,
        },
        app={
            'model'  : 'App',
            'icon'   : 'fontawesome.mobile-alt',
            'plural' : 'apps',
            'has'    : objects,
            'in'     : registry_objects,
            'links'  : links,
        },
        location={
            'model'  : 'Location',
            'icon'   : 'fontawesome.location-arrow',
            'plural' : 'locations',
            'has'    : objects,
            'in'     : registry_objects,
            'links'  : links,
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
    api=(
        ( r'ls/(?P<path>.*$)',       ( views.api_ls,     'ls',     [''] )),
        ( r'models/(?P<models>.*$)', ( views.api_models, 'models', [''] )),
        ( r'path/(?P<path>.*$)',     ( views.api_path,   'path',   [''] )),
        ( r'do/(?P<action>.+)/(?P<model>.+)/(?P<ids>.*)$',
                   ( views.api_do, 'do', [ 'list', 'friede.action', '' ])),
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
        ( 'actions',          views.ActionViewSet         ),
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
    serializers=(
        ( 'registry',       serializers.RegistrySerializer       ),
        ( 'container',      serializers.ContainerSerializer      ),
        ( 'widget',         serializers.WidgetSerializer         ),
        ( 'block',          serializers.BlockSerializer          ),
        ( 'screen',         serializers.ScreenSerializer         ),
        ( 'shell',          serializers.ShellSerializer          ),
        ( 'theme',          serializers.ThemeSerializer          ),
        ( 'slot',           serializers.SlotSerializer           ),
        ( 'app',            serializers.AppSerializer            ),
        ( 'icon',           serializers.IconSerializer           ),
        ( 'location',       serializers.LocationSerializer       ),
        ( 'link',           serializers.LinkSerializer           ),
        ( 'reference',      serializers.ReferenceSerializer      ),
        ( 'setting',        serializers.SettingSerializer        ),
        ( 'action',         serializers.ActionSerializer         ),
        ( 'containerentry', serializers.ContainerEntrySerializer ),
        ( 'widgetentry',    serializers.WidgetEntrySerializer    ),
        ( 'blockentry',     serializers.BlockEntrySerializer     ),
        ( 'screenentry',    serializers.ScreenEntrySerializer    ),
        ( 'shellentry',     serializers.ShellEntrySerializer     ),
        ( 'themeentry',     serializers.ThemeEntrySerializer     ),
        ( 'slotentry',      serializers.SlotEntrySerializer      ),
        ( 'appentry',       serializers.AppEntrySerializer       ),
        ( 'locationentry',  serializers.LocationEntrySerializer  ),
        ( 'iconentry',      serializers.IconEntrySerializer      ),
        ( 'linkentry',      serializers.LinkEntrySerializer      ),
        ( 'referenceentry', serializers.ReferenceEntrySerializer ),
        ( 'settingentry',   serializers.SettingEntrySerializer   ),
        ( 'actionentry',    serializers.ActionEntrySerializer    ),
    )
    @property
    def data( self ):
        return (
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
            ( 'from relations', self.objects, self.relations ),),
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
            ( 'apps',    dict( title='Apps',       href='/apps'    )),
            ( 'about',   dict( title='About Us',   href='/about'   )),
            ( 'contact', dict( title='Contact Us', href='/contact' )),
            ( 'from relations', self.objects, self.relations )),
          ( '#settings',
            ( 'from relations', self.objects, self.relations ),
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
              ( 'apps', dict(
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
        ( '0.2.0',
          ( '#actions',
            ( 'install', dict(
                icon='fontawesome.sign-in-alt',
                title='Install',
                description='''Incorporate the object into the system in some way''',
                data=dict(
                    reverse='uninstall',
                    widget='Installer',
                ))),
            ( 'uninstall', dict(
                icon='fontawesome.sign-out-alt',
                title='Uninstall',
                description='''Remove the object from the system''',
                data=dict(
                    reverse='install',
                    widget='Installer',
                ))),
            ( 'activate', dict(
                icon='fontawesome.toggle-on',
                title='Activate',
                description='''Enable the object to function''',
                data=dict(
                    reverse='deactivate',
                    widget='Activator',
                ))),
            ( 'deactivate', dict(
                icon='fontawesome.toggle-off',
                title='Deactivate',
                description='''Stop the object from functioning without removing it
                               completely''',
                data=dict(
                    reverse='activate',
                    widget='Activator',
                ))),
            ( 'update', dict(
                icon='fontawesome.sync-alt',
                title='Update',
                description='''Change the version of the object, if possible''',
                data=dict(
                    implies='upgrade',
                    widget='Installer',
                ))),
            ( 'upgrade', dict(
                icon='fontawesome.redo-alt',
                title='Upgrade',
                description='''Update the object to newer version''',
                data=dict(
                    reverse='downgrade',
                    widget='Installer',
                ))),
            ( 'downgrade', dict(
                icon='fontawesome.undo-alt',
                title='Downgrade',
                description='''Revert the object to an older version''',
                data=dict(
                    reverse='upgrade',
                    widget='Installer',
                ))),
          ),
          ( '#blocks',
            ( 'featured', dict(
                data=dict(
                    component='Centerfold'
                ))),
            ( 'grid', dict(
                data=dict(
                    component='GridDisplay'
                )),
              ( 'filtered', dict(
                  extends='grid',
                  data=dict(
                      component='FilterGrid'
                  )))),
            ( 'list', dict(
                data=dict(
                    component='ListDisplay'
                )),
              ( 'filtered', dict(
                  extends='list',
                  data=dict(
                      component='FilterList'
                  )))),
          ),
          ( '#screens',
            ( 'dashboard', dict(
                icon='fontawesome.columns',
                data=dict(
                    component='DashboardPage',
                )),
              ( 'from_model', dict(
                  icon='fontawesome.columns',
                  extends='dashboard',
                  data=dict(
                      component='ModelDashboard',
                  ))),
              ( 'apps', dict(
                  icon='fontawesome.rocket',
                  extends='dashboard.from_model',
                  data=dict(
                      actions=(
                          'install',
                          'activate',
                          'update',
                      ))),
                ( '#blocks',
                  ( 'breakfront', dict( path='featured' )),
                  ( 'content', dict( path='grid.filtered' ))),
              ),
              ( 'home', dict(
                  icon='fontawesome.home',
                  extends='dashboard',
                  data=dict(
                      component='HomeDashboard',
                  ))),
              ( 'user', dict(
                  icon='fontawesome.user',
                  extends='dashboard',
                  data=dict(
                      component='UserDashboard',
                  )),
                ( 'home', dict(
                    icon='fontawesome.bed',
                    extends='dashboard.user',
                    data=dict(
                        component='UserHomeDashboard',
                    ))),
              ))
          ),
          ( '#locations',
            ( 'home', {},
              ( '#screens',
                ( 'default', dict( path='dashboard.home' )))),
            ( 'apps', {},
              ( '#screens',
                ( 'default', dict(
                    path='dashboard.apps',
                    data=dict(
                        model='friede.app'
                    ))))),
          ),
        ),
        ( '0.2.1',
          ( '#actions',
            ( 'upgrade', dict( icon='fontawesome.level-up-alt' )),
            ( 'downgrade', dict( icon='fontawesome.level-down-alt' )),
          ),
          ( '#blocks',
            ( 'menu.sidebar', dict(
                icon='fontawesome',
                data=(
                    dict(
                        component='SidebarMenu'
                    )))),
            ( 'feed', dict(
                icon='fontawesome.rss',
                data=dict(
                    component='NewsFeed'
                )),
              ( 'site', dict(
                  icon='fontawesome.newspaper',
                  extends='feed',
                  data=dict(
                      source='site',
                  ))),
            ),
          ),
          ( '#screens',
            ( 'dashboard',
              ( 'home', {},
                ( '#blocks',
                  ( 'sidebar_left', dict(
                      path='menu.sidebar',
                      data=dict(
                          menu='site'
                      ))),
                  ( 'main', dict( path='feed.site' )))),
              ( 'apps', {},
                ( '#blocks',
                  ( 'content', dict(
                      path='grid.filtered',
                      rename='main' )))))
          ),
        ),
        ( '0.2.3',
          ( '#locations',
            ( 'apps', {},
              ( '#screens',
                ( 'default', dict(
                    path='dashboard.apps',
                    data=dict(
                        actions=(
                            'install',
                            'activate',
                            'update',
                        )),
                    entry=dict(
                        data=dict(
                            model='friede.app',
                            layout=dict(
                                title='title',
                                content='description'
                            ),
                            search='name title description'.split()
                        ))))))),
        ),
        ( '0.2.4',
          ( '#actions',
            ( 'install', dict(
                data=dict(
                    reverse='uninstall',
                    component='Installer',
                ))),
            ( 'uninstall', dict(
                data=dict(
                    reverse='install',
                    component='Installer',
                ))),
            ( 'activate', dict(
                data=dict(
                    reverse='deactivate',
                    component='Activator',
                ))),
            ( 'deactivate', dict(
                data=dict(
                    reverse='activate',
                    component='Activator',
                ))),
            ( 'update', dict(
                data=dict(
                    implies='upgrade',
                    component='Installer',
                ))),
            ( 'upgrade', dict(
                data=dict(
                    reverse='downgrade',
                    component='Installer',
                ))),
            ( 'downgrade', dict(
                data=dict(
                    reverse='upgrade',
                    component='Installer',
                ))),
          )
        ),
        ( '0.2.5',
          ( '#locations',
            ( 'apps', {},
              ( '#screens',
                ( 'default', dict(
                    path='dashboard.apps' ,
                    entry=dict(
                        data=dict(
                            model='friede.app',
                            layout=dict(
                                title='title',
                                subtitle='available',
                                content='description'
                            ),
                            search='name title description'.split()
                        )))))),
          ),
          ( '#actions',
            ( 'install', dict(
                data=dict(
                    reverse='uninstall',
                    component='Installer',
                    next='activate',
                    args=[ 'install_userdata' ]
                ))),
          )
        ),
        ( '0.2.6',            # empty version can be used to tag for update
        )
    )
    @property
    def userdata( self ):
        return ()

@action
def install( user, thing, userdata=True, **kw ):
    if not isinstance( thing, AppModel ):
        return                  # TODO: raise TypeError
    app = App.get_for_object( thing )
    app.install()
    if userdata:
        user_install( user, thing )

@action
def user_install( user, thing, **kw ):
    if isinstance( thing, UserApp ):
        thing = UserApp.app
    if not isinstance( thing, AppModel ):
        return                  # TODO: raise TypeError
    app = App.get_for_object( thing )
    if not app.installed:
        return                  # TODO: raise TypeError
    app.installuserdata( user )

@action
def uninstall( user, thing, **kw ):
    pass

@action
def user_uninstall( user, thing, **kw ):
    pass

@action
def update( user, thing, to='latest' **kw ):
    if not isinstance( thing, AppModel ):
        return                  # TODO: raise TypeError
    app = App.get_for_object( thing )
    if not app.installed:
        return                  # todo raise TypeError
    app.update()
    v = version_parse( to )
    app.upgrade( to=app.available if to == 'latest' else to if v.release
                 else app.versions.get( to ))
    

@action
def upgrade( user, thing, **kw ):
    pass

@action
def downgrade( user, thing, **kw ):
    pass

@action
def activate( user, thing, **kw ):
    pass

@action
def user_activate( user, thing, **kw ):
    pass

@action
def deactivate( user, thing, **kw ):
    pass

@action
def user_deactivate( user, thing, **kw ):
    pass

