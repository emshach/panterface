# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from . import views
from .core import installapp
from .models import App, Setting
from importlib import import_module
from rest_framework import routers

app_name = 'friede'
urlpatterns = []
router = routers.DefaultRouter()
router.register( r'containers', views.ContainerViewSet )
router.register( r'widgets',    views.WidgetViewSet    )
router.register( r'blocks',     views.BlockViewSet     )
router.register( r'screens',    views.ScreenViewSet    )
router.register( r'shells',     views.ShellViewSet     )
router.register( r'themes',     views.ThemeViewSet     )
router.register( r'slots',      views.SlotViewSet      )
router.register( r'apps',       views.AppViewSet       )
router.register( r'locations',  views.LocationViewSet  )
router.register( r'links',      views.LinkViewSet      )
router.register( r'references', views.ReferenceViewSet )
router.register( r'settings',   views.SettingViewSet   )

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
            ( '.apps',    dict( title='Apps',       href='/apps'    )),
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
                extends='adaptive',
                data=dict(
                    component='ViewModelWidget'
                ))),
            ( 'new.from.model', dict(
                extends='adaptive',
                data=dict(
                    component='NewModelWidget'
                ))),
            ( 'edit.from.model', dict(
                extends='adaptive',
                data=dict(
                    component='EditModelWidget'
                ))),
            ( 'report.from.model', dict(
                extends='adaptive',
                data=dict(
                    component='ReportModelWidget'
                ))),
            ( 'delete.from.model', dict(
                extends='adaptive',
                data=dict(
                    component='ReportModelWidget'
                ))),
            tuple(
                ( action,
                  tuple(( o, dict(
                      extends="{}.from.model".format( action ),
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


apps = App.objects.filter( active=True ).all()
for app in apps:
    name = app.name
    module = app.module
    rest = app.rest
    if module:
        try:
            urls = import_module( "%s.%s" % ( module, 'urls' ))
            if rest:
                router = urls.router
                match = r'^api/%s/' % name
                urlpatterns.append( url( match, include( router.urls )))
        except ImportError, AttributeError:
            continue

urlpatterns.append( url( r'^.*$', views.index, name='index' ))
