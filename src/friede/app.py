# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from importlib import import_module
from rest_framework import routers, relations
from collections import OrderedDict
from packaging.version import _BaseVersion
from django.conf import settings
from .core import installappheader, installapp, updateapp, upgradeapp
from .models import App, UserApp, Setting
from .views import lookup
from .action import action, actions, Action
from .util import toversion
from . import views
import traceback
import sys

original_reverse = relations.reverse

def hack_reverse( alias, **kwargs ):
    namespace = kwargs[ 'request' ].resolver_match.namespace
    name = "%s:%s" % ( namespace, alias )
    return original_reverse( name, **kwargs )

relations.reverse = hack_reverse

router = routers.DefaultRouter()
routes = OrderedDict()
apps = OrderedDict()

def namespace( thing, name ):
    if name not in thing:
        thing[ name ] = OrderedDict()
    return thing[ name ]

def load( name, urlpatterns ):
    module = name
    if not name: return
    app = apps.get( name )
    if app: return app
    try:
        apps[ name ] = 'loading'
        app = import_module( "%s.friede_app" % module )
        app = app.App()
        apps[ app.name ] = app
        if not name == app.name:
            apps[ name ] = app
        if app.installed:
            myroutes = namespace( routes, app.name )
            mylookup = namespace( lookup, app.name )
            return app.init( myroutes, mylookup, router, urlpatterns )
    except ( ImportError, AttributeError ) as e:
        msg = str(e)
        if 'No module named friede_app' not in msg:
            apps[ name ] = 'error'
            print >> sys.stderr, 'got exception', type(e), e,\
                "in friede.urls/%s" % module

def setup( urlpatterns ):
    from . import friede_app
    try:
        apps[ 'friede' ] = 'loading'
        friede = friede_app.App()
        apps[ 'friede' ] = friede
        friede.install()
        myroutes = namespace( routes, 'friede' )
        mylookup = namespace( lookup, 'friede' )
        friede.init( myroutes, mylookup, router, urlpatterns )
        for app_name in settings.INSTALLED_APPS:
            if not app_name == 'friede':
                load( app_name, urlpatterns )
    except Exception:
        # pass                        # TODO: handle
        raise

class NamedDefaultRouter( routers.DefaultRouter ):
    def __init__( self, name, *args, **kwargs ):
        # self.root_view_name = "api-root-%s" % name
        super( NamedDefaultRouter, self ).__init__( *args, **kwargs )


class App( object ) :
    name = ''
    icon = ''
    module = ''
    title = ''
    description = ''
    objects = ()
    relations = ()
    actions = ()
    api = ()
    routes = ()
    router = None
    serializers = ()
    model=None
    required = False
    user_required = False
    user_installable = True
    auto_install = False
    auto_user_install = False

    def __init__( self ):
        super( App, self ).__init__()
        self.preinstallheader()
        self.model, _ = self.installheader()
        self.versions=OrderedDict()
        self.version = self.model.version
        if self.model:
            self.postinstallheader()
            self.preupdate()
            self.update()
            self.postupdate()
        if self.required or self.auto_install:
            self.install()
        if self.required:
            self.activate()
        # TODO: else raise exception

    def __nonzero__( self ): return True

    def preinstallheader( self ):
        pass

    def installheader( self ):
        return installappheader(
            name=self.name,
            icon=self.icon,
            module=self.module,
            title=self.title,
            description=self.description,
            min_version=self.min_version,
            required=self.required,
            user_required=self.user_required,
            user_installable=self.user_installable,
            auto_install=self.auto_install,
        )

    def postinstallheader( self ):
        if self.min_version:
            self.versions[ 'default' ] = toversion( self.min_version )
        if self.model.installed:
            self.versions[ 'current' ] = toversion( self.model.version )
        else:
            self.versions.pop( 'current', None )

    def preinstall( self ):
        pass

    def install( self ):
        ret = installapp(
            name=self.name,
            icon=self.icon,
            module=self.module,
            title=self.title,
            description=self.description,
            data=self.data,
            obj=self
        )
        if self.model.version != '0.0.0':
            self.model.installed = True
            self.model.save()
        return ret

    def postinstall( self ):
        if self.model.installed:
            self.versions[ 'current' ] = toversion( self.model.version )
        else:
            self.versions.pop( 'current', None )

    def activate( self ):
        if self.model:
            self.model.active = True
            self.model.save()

    def deactivate( self ):
        if self.model:
            self.model.active = False
            self.model.save()

    def preinit( self ):
        pass

    def init( self, routes, lookup, router=None, urlpatterns=None ):
        name = self.name
        self.router = routes[ name ] = NamedDefaultRouter( name )
        lookup[ name ] = 'api-root'

        for k, v in self.api:
            routes[k] = v[ 0 : 2 ]
            lookup[ v[1] ] = v[ 1: ]

        for k, v in self.routes:
            self.router.register( k, v )

        return self

    def preupdate( self ):
        pass

    def update( self ):
        return updateapp( self.name, self.data, self )

    def postupdate( self ):
        if toversion( self.version ) < toversion( self.min_version )\
           and self.auto_install:
            self.preupgrade()
            self.upgrade( to=self.min_version )
            self.postupgrade()

    def preupgrade( self ):
        pass

    def upgrade( self, to=None ):
        return upgradeapp( self.model, self.data, to )

    def postupgrade( self ):
        self.version = self.model.version
        if self.model.installed:
            self.versions[ 'current' ] = toversion( self.model.version )
        else:
            self.versions.pop( 'current', None )
        pass

    def predowngrade( self ):
        pass

    def downgrade( self ):
        pass

    def postdowngrade( self ):
        pass

    def postinit( self ):
        pass

    def preuninstall( self ):
        pass

    def uninstall( self ):
        pass

    def postuninstall( self ):
        pass

    def preremove( self ):
        pass

    def remove( self ):
        pass

    def postremove( self ):
        pass

    def install_for_user( self, user=None, userapp=None ):
        pass

    def update_for_user( self, user=None, userapp=None ):
        pass

    def uninstall_for_user( self, user=None, userapp=None ):
        pass

    def activate_for_user( self, user=None, userapp=None ):
        pass

    def deactivate_for_user( self, user=None, userapp=None ):
        pass

    def setversionmeta( self, version, field, value ):
        v = self.versions
        if version not in v:
            v[ version ] = {}
            if 'latest' not in v or version > v[ 'latest' ]:
                v[ 'latest' ] = version
        v[ version ][ field ] = value

    def getversions( self, match=None, op=None ):
        if match is None:
            return filter( lambda x: isinstance( x, _BaseVersion ), self.versions )
        # m = match
        meta = None
        seen = set()
        if ' ' in match:
            op1, match = match.split()
            if not op:
                op = op1 or '>='
        if not match:
            return None
        if op in ( '=', '==' ):
            def op(x):
                return isinstance( x, _BaseVersion ) and x == match
        elif op == '!=':
            def op(x):
                return isinstance( x, _BaseVersion ) and x != match
        elif op == '>':
            def op(x):
                return isinstance( x, _BaseVersion ) and x > match
        elif op == '>=':
            def op(x):
                return isinstance( x, _BaseVersion ) and x >= match
        elif op == '<':
            def op(x):
                return isinstance( x, _BaseVersion ) and x < match
        elif op == '<=':
            def op(x):
                return isinstance( x, _BaseVersion ) and x <= match
        else:
            return None         # maybe rayse invalid op
        while isinstance( match, basestring ) and match in self.versions:
            if match in seen:
                return None     # cyclic def, maybe definitely raise
            seen.add( match )
            match = self.versions[ match ]
        if not isinstance( match, _BaseVersion ):
            match = toversion( match )
        return filter( op, self.versions )

    @property
    def available( self ):
        return toversion( self.model.available ) if self.model else None

    @property
    def installed( self ):
        return self.model.installed

    @property
    def active( self ):
        return self.model.active

    @property
    def data( self ):
        return None

    @property
    def version( self ):
        return toversion( self.model.version if self.model else '0.0.0' )

    @version.setter
    def version( self, version ):
        if self.model:
            self.model.version = str( version )
            self.model.save()

    @property
    def min_version( self ):
        return toversion( self.model.min_version if self.model else '0.0.0' )

    @version.setter
    def min_version( self, min_version ):
        if self.model:
            self.model.min_version = str( min_version )
            self.model.save()

    @staticmethod
    def get_for_object( object ):
        if isinstance( object, UserApp ):
            object = object.app
        name = object.path
        if name.startswith( 'apps.' ):
            name = name[ 5: ]
        return apps[ name ]

    @staticmethod
    def get_for_user( object, user ):
        if isinstance( object, UserApp ):
            if ( object.user is user ):
                return object
            object = object.app
        userapp, new = UserApp.get_or_create( app=object, user=user )
        return userapp
