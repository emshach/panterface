# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from importlib import import_module
from rest_framework import routers, relations
from collections import OrderedDict
from packaging.version import parse as version_parse
from . import views
from .core import installappheader, installapp, updateapp, upgradeapp
from .models import App, Setting
from .views import routes as view_routes

original_reverse = relations.reverse

def hack_reverse( alias, **kwargs ):
    namespace = kwargs[ 'request' ].resolver_match.namespace
    name = "%s:%s" % ( namespace, alias )
    return original_reverse( name, **kwargs )

relations.reverse = hack_reverse

router = routers.DefaultRouter()
routes = OrderedDict()
apps = OrderedDict()

class NamedDefaultRouter( routers.DefaultRouter ):
    def __init__( self, name, *args, **kwargs ):
        self.root_view_name = "api-root-%s" % name
        super( NamedDefaultRouter, self ).__init__( *args, **kwargs )

def registrar( router, routes, app ):
    name = app.name
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


class App( object ) :
    installed = False
    name = ''
    icon = ''
    module = ''
    title = ''
    description = ''
    objects = ()
    relations = ()
    actions = ()
    routes = ()
    serializers = ()
    model=None
    version='0.0.0'
    min_version='0.0.1'
    required = False
    user_required = False
    user_installable = True
    auto_install = False
    auto_user_install = False

    def __init__( self ):
        self.preinstallheader()
        self.model, _ = self.installheader()
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
        pass

    def preinstall( self ):
        pass

    def install( self ):
        return installapp(
            name=self.name,
            icon=self.icon,
            module=self.module,
            title=self.title,
            description=self.description,
            data=self.data
        )

    def postinstall( self ):
        pass

    def activate( self ):
        if self.model:
            self.model.active = True
            self.model.save()

    def preinit( self ):
        pass

    def init( self, register, router=None, urlpatterns=None ):
        for k, v in self.routes:
            register( k, v )

    def preupdate( self ):
        pass

    def update( self ):
        return updateapp( self.name, self.data, self )

    def postupdate( self ):
        if version_parse( self.version ) < version_parse( self.min_version ):
            self.preupgrade()
            self.upgrade( to=self.min_version )
            self.postupgrade()

    def preupgrade( self ):
        pass

    def upgrade( self, to=None ):
        return upgradeapp( self.model, self.data, to )

    def postupgrade( self ):
        self.version = self.model.version
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

    @property
    def data( self ):
        return None
