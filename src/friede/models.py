# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
    name         = M.SlugField( blank=True )
    title        = M.CharField( blank=True, max_length=255 )
    icon         = M.CharField( blank=True, max_length=255 )
    description  = M.TextField( blank=True )
    active       = M.BooleanField( default=True )

    def __str__( self ):
        return self.name or self.title

    def getcontext( self ):
        return self


class Registry( Base ):
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

    def addcontainer( name, container ):
        ContainerEntry.create( registry=self, name=name, container=container )

    def addwidget( name, widget ):
        WidgetEntry.create( registry=self, name=name, widget=widget )

    def addblock( name, block ):
        BlockEntry.create( registry=self, name=name, block=block )

    def addscreen( name, screen ):
        ScreenEntry.create( registry=self, name=name, screen=screen )

    def addshell( name, shell ):
        ShellEntry.create( registry=self, name=name, shell=shell )

    def addtheme( name, theme ):
        ThemeEntry.create( registry=self, name=name, theme=theme )

    def addslot( name, slot ):
        SlotEntry.create( registry=self, name=name, slot=slot )

    def addapp( name, app ):
        AppEntry.create( registry=self, name=name, app=app )

    def addlocation( name, location ):
        LocationEntry.create( registry=self, name=name, location=location )

    def addlink( name, link ):
        LinkEntry.create( registry=self, name=name, link=link )

    def addreference( name, reference ):
        ReferenceEntry.create( registry=self, name=name, reference=reference )

    def addsetting( name, setting ):
        SettingEntry.create( registry=self, name=name, setting=setting )


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


class Location( Base ):
    registry = M.ManyToManyField( Registry, blank=True, through='LocationEntry',
                                  related_name='_locations' )


class Link( Base ):
    registry = M.ManyToManyField( Registry, blank=True, through='LinkEntry',
                                  related_name='links' )
    location = M.ForeignKey( Location, M.SET_NULL, null=True, blank=True,
                             related_name='_links' )


class Reference( Base ):
    registry = M.ManyToManyField( Registry, blank=True, through='ReferenceEntry',
                                  related_name='_references' )
    target = M.CharField( max_length=255 )

    def resolve( self ):
        return Registry.objects.get( name=self.target )
    # TODO: trycatch


class Setting( Base ):
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


class ContainerEntry( Base ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_container_entries' )
    container = M.ForeignKey( Container, M.CASCADE, related_name='_entries' )


class WidgetEntry( Base ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_widget_entries' )
    widget = M.ForeignKey( Widget, M.CASCADE, related_name='_entries' )


class BlockEntry( Base ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_block_entries' )
    block = M.ForeignKey( Block, M.CASCADE, related_name='_entries' )


class ScreenEntry( Base ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_screen_entries' )
    screen = M.ForeignKey( Screen, M.CASCADE, related_name='_entries' )


class ShellEntry( Base ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_shell_entries' )
    shell = M.ForeignKey( Shell, M.CASCADE, related_name='_entries' )


class ThemeEntry( Base ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_theme_entries' )
    theme = M.ForeignKey( Theme, M.CASCADE, related_name='_entries' )


class SlotEntry( Base ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_slot_entries' )
    slot = M.ForeignKey( Slot, M.CASCADE, related_name='_entries' )


class AppEntry( Base ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_app_entries' )
    app = M.ForeignKey( App, M.CASCADE, related_name='_entries' )


class LocationEntry( Base ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_location_entries' )
    location = M.ForeignKey( Location, M.CASCADE, related_name='_entries' )


class LinkEntry( Base ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_link_entries' )
    link = M.ForeignKey( Link, M.CASCADE, related_name='_entries' )


class ReferenceEntry( Base ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_reference_entries' )
    reference = M.ForeignKey( Reference, M.CASCADE, related_name='_entries' )


class SettingEntry( Base ):
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_setting_entries' )
    setting = M.ForeignKey( Setting, M.CASCADE, related_name='_entries' )


