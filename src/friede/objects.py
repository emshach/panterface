# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import ( Registry, Container, Widget, Block, Screen, Shell,
                      Theme, Slot, App, Location, Link, Reference, Setting,
                      ContainerEntry )
from .util import snake_case
from django.core.exceptions import ObjectDoesNotExist

class Selector( object ):
    def __init__( self, root, type=Container, field=None, entries=None ):
        super( Selector, self ).__init__()
        self.root = root if isinstance( root, ( list, tuple )) else ( root, )
        self.type = type
        # TODO: if not type, error
        if field:
            self.field = field
        elif hasattr( self.type, '_name' ):
            self.field = self.type._name
        else:
            self.field = "_%s" % snake_case( self.type.__name__ )
        if entries:
            self.entries = entries
        else:
            self.entries = "%s_entries" % self.field

    def get( self ):
        if not len( self.root ):
            return None
        new = []
        for item in self.root:
            if isinstance( item, self.type ):
                new.append( item )
                continue
            item = getattr( item, self.field, None )
            if isinstance( item, self.type ):
                new.append( item )
        if not len( new ):
            new = [ x for x in self.root if isinstance( x, Container )]

        if len( new ) == 1:
            return new[0]
        elif len( new ):
            return new
        else:
            return None

    def __getattr__( self, attr ):
        if not len( self.root ):
            return self
        new = []
        for item in self.root:
            if type( item ) is Registry and item._container:
                item = item._container
            if not isinstance( item, Registry ): # TODO: fingers crossed
                continue
            "then try get entries with this name"
            try:
                node = item._container_entries.get( name=attr ).entry
                new.append( node )
            except ContainerEntry.DoesNotExist:
                pass
            if self.type is not Container:
                try:
                    node = getattr( item, self.entries ).get( name=attr).entry
                    new.append( node )
                except ObjectDoesNotExist:
                    pass
        return Selector( new, type=self.type, field=self.field, entries=self.entries )

    def __call__( self, *args ):
        if not len( args ):
            return self.get()
        if len( args ) == 1:
            return getattr( self, args[0] ) if args[0] else self
        return getattr( self, args[0] )( *args[1:] )


class CreatingSelector( Selector ):
    def __init__( self, name, type, parent=None ):
        if not isinstance( parent, Registry ):
            parent = None
        obj, created = Container.objects.get_or_create(
            name=name,
            parent=parent )
        super( CreatingSelector, self ).__init__( obj, type=type )


class Containers( CreatingSelector ):
    def __init__( self ):
        super( Containers, self ).__init__( 'containers', Container )


class Widgets( CreatingSelector ):
    def __init__( self ):
        super( Widgets, self ).__init__( 'widgets', Widget )


class Blocks( CreatingSelector ):
    def __init__( self ):
        super( Blocks, self ).__init__( 'blocks', Block )


class Screens( CreatingSelector ):
    def __init__( self ):
        super( Screens, self ).__init__( 'screens', Screen )


class Shells( CreatingSelector ):
    def __init__( self ):
        super( Shells, self ).__init__( 'shells', Shell )


class Themes( CreatingSelector ):
    def __init__( self ):
        super( Themes, self ).__init__( 'themes', Theme )


class Slots( CreatingSelector ):
    def __init__( self ):
        super( Slots, self ).__init__( 'slots', Slot )


class Apps( CreatingSelector ):
    def __init__( self ):
        super( Apps, self ).__init__( 'apps', App )


class Locations( CreatingSelector ):
    def __init__( self ):
        super( Locations, self ).__init__( 'locations', Location )


class Links( CreatingSelector ):
    def __init__( self ):
        super( Links, self ).__init__( 'links', Link )


class References( CreatingSelector ):
    def __init__( self ):
        super( References, self ).__init__( 'references', Reference )


class Settings( CreatingSelector ):
    def __init__( self ):
        super( Settings, self ).__init__( 'settings', Setting )


def getregistries():
    return Container.objects.filter( parent__isnull=True ).all()

def getshell( *args ):
    return Shell().get( *args )

def getenv():
    env, created = Container.objects.get_or_create( name='env', parent__isnull=True )
    return env
