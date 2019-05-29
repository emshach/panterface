# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from importlib import import_module
from rest_framework import routers, relations
from collections import OrderedDict
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
    model=None

    def __init__( self ):
        self.preinstallheader()
        self.model, _ = self.installheader()
        if self.model:
            self.postinstallheader()
            self.preupdate()
            self.update()
            self.postupdate()
        # TODO: else raise exception

    def preinstallheader( self ):
        pass

    def installheader( self ):
        return installappheader(
            name=self.name,
            icon=self.icon,
            module=self.module,
            title=self.title,
            description=self.description,
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
            data=self.getdata()
        )

    def postinstall( self ):
        pass

    def preinit( self ):
        pass

    def init( self, register, router=None, urlpatterns=None ):
        for k, v in self.routes:
            register( k, v )

    def preupdate( self ):
        pass

    def update( self ):
        return updateapp( self.name, self.getdata() )

    def postupdate( self ):
        pass

    def preupgrade( self ):
        pass

    def upgrade( self, to=None ):
        return upgradeapp( self.model, self.getdata(), to )

    def postupgrade( self ):
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

    def getdata( self ):
        return None
