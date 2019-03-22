# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .util import snake_case
from django.contrib.auth import get_user_model
from django.utils.encoding import python_2_unicode_compatible
from django.db import models as M
from django.contrib.postgres.fields import JSONField
from datetime import date
from django.utils.timezone import now


Model = M.Model

@python_2_unicode_compatible
class Base( Model ):
    class Meta:
        abstract = True
    name         = M.SlugField()
    title        = M.CharField( blank=True, max_length=255 )
    icon         = M.CharField( blank=True, max_length=255 )
    description  = M.TextField( blank=True )
    active       = M.BooleanField( default=True )

    def __str__( self ):
        return self.name or self.title

    def getcontext( self ):
        return self

class Path( Model ):
    class Meta:
        abstract = True
    path = M.CharField( max_length=255 )

    # override save
    def save( self, *args, **kwargs ):
        created = False
        if not self.path and self.name and '.' in self.name:
            self.path = self.name
        if self.path:
            "make sure we're properly attached"
            path = self.path.split('.')
            if len( path ) > 1:
                self.name = path.pop()
                self.parent, created = Container.objects.get_or_create( path='.'.join( path  ))
            else:
                self.parent = None
                self.name = path[0]
        elif self.name:
            "make path if we have parent"
            if self.parent:
                self.path = "%s.%s" % ( self.parent.path, self.name )
            else:
                self.path = self.name
        super( Path, self ).save( *args, **kwargs )
        if not self.parent:
            return
        if self._entries.filter( registry=self.parent ).count():
            return
        self._entries.model.objects.create(
            registry=self.parent,
            entry=self,
            name=self.name
        )

class Registry( Base, Path ):
    format = JSONField( default=list )
    default = JSONField( default=list )
    parent = M.ForeignKey( 'self', M.CASCADE, null=True, related_name='_elements' )

    @property
    def Container( self ):
        from .objects import Selector
        return Selector( self, Container )

    @property
    def Widget( self ):
        from .objects import Selector
        return Selector( self, Widget )

    @property
    def Block( self ):
        from .objects import Selector
        return Selector( self, Block )

    @property
    def Screen( self ):
        from .objects import Selector
        return Selector( self, Screen )

    @property
    def Shell( self ):
        from .objects import Selector
        return Selector( self, Shell )

    @property
    def Theme( self ):
        from .objects import Selector
        return Selector( self, Theme )

    @property
    def Slot( self ):
        from .objects import Selector
        return Selector( self, Slot )

    @property
    def App( self ):
        from .objects import Selector
        return Selector( self, App )

    @property
    def Location( self ):
        from .objects import Selector
        return Selector( self, Location )

    @property
    def Link( self ):
        from .objects import Selector
        return Selector( self, Link )

    @property
    def Reference( self ):
        from .objects import Selector
        return Selector( self, Reference )

    @property
    def Setting( self ):
        from .objects import Selector
        return Selector( self, Setting )

    C = Container
    W = Widget
    B = Block
    S = Screen
    H = Shell
    T = Theme
    O = Slot
    A = App
    L = Location
    K = Link
    R = Reference
    X = Setting

    def addcontainer( self, name, container ):
        ContainerEntry.objects.create( registry=self, name=name, entry=container )

    def addwidget( self, name, widget ):
        WidgetEntry.objects.create( registry=self, name=name, entry=widget )

    def addblock( self, name, block ):
        BlockEntry.objects.create( registry=self, name=name, entry=block )

    def addscreen( self, name, screen ):
        ScreenEntry.objects.create( registry=self, name=name, entry=screen )

    def addshell( self, name, shell ):
        ShellEntry.objects.create( registry=self, name=name, entry=shell )

    def addtheme( self, name, theme ):
        ThemeEntry.objects.create( registry=self, name=name, entry=theme )

    def addslot( self, name, slot ):
        SlotEntry.objects.create( registry=self, name=name, entry=slot )

    def addapp( self, name, app ):
        AppEntry.objects.create( registry=self, name=name, entry=app )

    def addlocation( self, name, location ):
        LocationEntry.objects.create( registry=self, name=name, entry=location )

    def addlink( self, name, link ):
        LinkEntry.objects.create( registry=self, name=name, entry=link )

    def addreference( self, name, reference ):
        ReferenceEntry.objects.create( registry=self, name=name, entry=reference )

    def addsetting( self, name, setting ):
        SettingEntry.objects.create( registry=self, name=name, entry=setting )


class Container( Registry ):
    registry_ptr  = M.OneToOneField( Registry, M.CASCADE, parent_link=True,
                                     related_name='_container' )
    registry = M.ManyToManyField( Registry, blank=True, through='ContainerEntry',
                                  related_name='_containers' )


class Widget( Registry ):
    registry_ptr  = M.OneToOneField( Registry, M.CASCADE, parent_link=True,
                                     related_name='_widget' )
    registry = M.ManyToManyField( Registry, blank=True, through='WidgetEntry',
                                  related_name='_widgets' )


class Block( Registry ):
    registry_ptr  = M.OneToOneField( Registry, M.CASCADE, parent_link=True,
                                     related_name='_block' )
    registry = M.ManyToManyField( Registry, blank=True, through='BlockEntry',
                                  related_name='_blocks' )


class Screen( Registry ):
    registry_ptr  = M.OneToOneField( Registry, M.CASCADE, parent_link=True,
                                     related_name='_screen' )
    registry = M.ManyToManyField( Registry, blank=True, through='ScreenEntry',
                                  related_name='_screens' )


class Shell( Registry ):
    registry_ptr  = M.OneToOneField( Registry, M.CASCADE, parent_link=True,
                                     related_name='_shell' )
    registry = M.ManyToManyField( Registry, blank=True, through='ShellEntry',
                                  related_name='_shells' )
    templates = M.CharField( max_length=255 ) # TODO: default
    template = M.CharField( max_length=255, default='index.html' )

    @property
    def home( self ):
        return "%s/%s" % ( self.templates, self.template )


class Theme( Registry ):
    registry_ptr  = M.OneToOneField( Registry, M.CASCADE, parent_link=True,
                                     related_name='_theme' )
    registry = M.ManyToManyField( Registry, blank=True, through='ThemeEntry',
                                  related_name='_themes' )
    templates = M.CharField( max_length=255 ) # TODO: default
    template = M.CharField( max_length=255, default='index.html' )

    @property
    def home( self ):
        return "%s/%s" % ( self.templates, self.template )


class Slot( Registry ):
    registry_ptr  = M.OneToOneField( Registry, M.CASCADE, parent_link=True,
                                     related_name='_slot' )
    registry = M.ManyToManyField( Registry, blank=True, through='SlotEntry',
                                  related_name='_slots' )


class App( Registry ):
    registry_ptr  = M.OneToOneField( Registry, M.CASCADE, parent_link=True,
                                     related_name='_app' )
    registry = M.ManyToManyField( Registry, blank=True, through='AppEntry',
                                  related_name='_apps' )


class Location( Base, Path ):
    registry = M.ManyToManyField( Registry, blank=True, through='LocationEntry',
                                  related_name='_locations' )


class Link( Base, Path ):
    registry = M.ManyToManyField( Registry, blank=True, through='LinkEntry',
                                  related_name='links' )
    location = M.ForeignKey( Location, M.SET_NULL, null=True, blank=True,
                             related_name='_links' )


class Reference( Base, Path ):
    registry = M.ManyToManyField( Registry, blank=True, through='ReferenceEntry',
                                  related_name='_references' )
    target = M.CharField( max_length=255 )

    def resolve( self ):
        return Registry.objects.get( name=self.target )
    # TODO: trycatch


class Setting( Base, Path ):
    class Types:
        BOOLEAN             = 'BooleanField'
        CHAR                = 'CharField'
        CHOICE              = 'ChoiceField'
        TYPEDCHOICE         = 'TypedChoiceField'
        DATE                = 'DateField'
        DATETIME            = 'DateTimeField'
        DECIMAL             = 'DecimalField'
        DURATION            = 'DurationField'
        EMAIL               = 'EmailField'
        FILE                = 'FileField'
        FILEPATH            = 'FilePathField'
        FLOAT               = 'FloatField'
        IMAGE               = 'ImageField'
        INTEGER             = 'IntegerField'
        IPADDRESS           = 'GenericIPAddressField'
        MULTIPLECHOICE      = 'MultipleChoiceField'
        TYPEDMULTIPLECHOICE = 'TypedMultipleChoiceField'
        NULLBOOLEAN         = 'NullBooleanField'
        REGEX               = 'RegexField'
        SLUG                = 'SlugField'
        TIME                = 'TimeField'
        URL                 = 'URLField'
        UUID                = 'UUIDField'
        COMBO               = 'ComboField'
        VALUES              = 'MultiValueField'
        SPLITDATETIME       = 'SplitDateTimeField'
        MODEL               = 'ModelChoiceField'
        MODELS              = 'ModelMultipleChoiceField'

        ALL = (
            ( BOOLEAN,             'True/False' ),
            ( CHAR,                'String' ),
            ( CHOICE,              'Choice' ),
            ( TYPEDCHOICE,         'Choice (typed)' ),
            ( DATE,                'Date' ),
            ( DATETIME,            'Date and time' ),
            ( DECIMAL,             'Decibal' ),
            ( DURATION,            'Duration' ),
            ( EMAIL,               'Email' ),
            ( FILE,                'File' ),
            ( FILEPATH,            'File-path' ),
            ( FLOAT,               'Fraction' ),
            ( IMAGE,               'Image' ),
            ( INTEGER,             'Integer' ),
            ( IPADDRESS,           'IP Address' ),
            ( MULTIPLECHOICE,      'Multiple Choice' ),
            ( TYPEDMULTIPLECHOICE, 'Multiple Choice (typed)' ),
            ( NULLBOOLEAN,         'True/False/Null' ),
            ( REGEX,               'Regular Expression' ),
            ( SLUG,                'Slug' ),
            ( TIME,                'Time' ),
            ( URL,                 'URL' ),
            ( UUID,                'UUID' ),
            ( COMBO,               'Combo' ),
            ( VALUES,              'Multiple Values' ),
            ( SPLITDATETIME,       'Split date and time' ),
            ( MODEL,               'Model Choice' ),
            ( MODELS,              'Multiple Model Choice' ),
        )
    registry = M.ManyToManyField( Registry, blank=True, through='SettingEntry',
                                  related_name='_settings' )
    type     = M.CharField( max_length=32, choices=Types.ALL, default=Types.CHAR )
    default  = JSONField( default=dict )
    data     = JSONField( default=dict )


class Entry( Base ):
    class Meta:
        unique_together = ( 'registry', 'name' )
        abstract = True

class ContainerEntry( Entry ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_container_entries' )
    entry = M.ForeignKey( Container, M.CASCADE, related_name='_entries' )


class WidgetEntry( Entry ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_widget_entries' )
    entry = M.ForeignKey( Widget, M.CASCADE, related_name='_entries' )


class BlockEntry( Entry ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_block_entries' )
    entry = M.ForeignKey( Block, M.CASCADE, related_name='_entries' )


class ScreenEntry( Entry ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_screen_entries' )
    entry = M.ForeignKey( Screen, M.CASCADE, related_name='_entries' )


class ShellEntry( Entry ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_shell_entries' )
    entry = M.ForeignKey( Shell, M.CASCADE, related_name='_entries' )


class ThemeEntry( Entry ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_theme_entries' )
    entry = M.ForeignKey( Theme, M.CASCADE, related_name='_entries' )


class SlotEntry( Entry ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_slot_entries' )
    entry = M.ForeignKey( Slot, M.CASCADE, related_name='_entries' )


class AppEntry( Entry ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_app_entries' )
    entry = M.ForeignKey( App, M.CASCADE, related_name='_entries' )


class LocationEntry( Entry ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_location_entries' )
    entry = M.ForeignKey( Location, M.CASCADE, related_name='_entries' )


class LinkEntry( Entry ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_link_entries' )
    entry = M.ForeignKey( Link, M.CASCADE, related_name='_entries' )


class ReferenceEntry( Entry ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_reference_entries' )
    entry = M.ForeignKey( Reference, M.CASCADE, related_name='_entries' )


class SettingEntry( Entry ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_setting_entries' )
    entry = M.ForeignKey( Setting, M.CASCADE, related_name='_entries' )


