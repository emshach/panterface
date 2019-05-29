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
class _Base( Model ):
    class Meta:
        abstract = True
    name         = M.SlugField()
    title        = M.CharField( blank=True, max_length=255 )
    description  = M.TextField( blank=True )
    active       = M.BooleanField( default=True )

    def __str__( self ):
        return getattr( self, 'path', None ) or self.name or self.title

    def getcontext( self ):
        return self

    def to_dict( self ):
        out = {
            '$name'        : self.name,
            '$title'       : self.title,
            '$description' : self.description,
        }
        if hasattr( self, 'path' ):
            out[ '$path' ] = self.path
        return out

class Base( _Base ):
    class Meta:
        abstract = True
    icon         = M.ForeignKey( 'Icon', blank=True, null=True )

class PathMixin( Model ):
    class Meta:
        abstract = True
    path = M.CharField( max_length=255 )

    # override save
    def save( self, *args, **kwargs ):
        created = False
        container = None
        if not self.path and self.name and '.' in self.name:
            self.path = self.name
        if self.path:
            "make sure we're properly attached"
            path = self.path.split('.')
            if len( path ) > 1:
                self.name = path.pop()
                self.parent, created = Container.objects.get_or_create(
                    path='.'.join( path ))
            else:
                self.parent = None
                self.name = path[0]
        elif self.name:
            "make path if we have parent"
            if getattr( self, 'parent', getattr( self, 'registry', None )):
                self.path = "%s.%s" % ( self.parent.path, self.name )
            else:
                self.path = self.name
        super( PathMixin, self ).save( *args, **kwargs )
        if not self.parent:
            return
        if self._entries.filter( registry=self.parent ).count():
            return
        entry, created = self._entries.model.objects.get_or_create(
            registry=self.parent,
            name=self.name,
            defaults=dict( entry=self ))
        if not created:
            entry.entry = self
            entry.save()


class SizeMixin( Model ):
    class Meta:
        abstract = True
    min_x = M.PositiveSmallIntegerField( default=1 )
    max_x = M.PositiveSmallIntegerField( blank=True, null=True )
    min_y = M.PositiveSmallIntegerField( default=1 )
    max_y = M.PositiveSmallIntegerField( blank=True, null=True )


class DataMixin( Model ):
    class Meta:
        abstract = True
    data = JSONField( default=dict )


class ExtendsMixin( Model ):
    class Meta:
        abstract = True
    extends = M.ForeignKey( 'self', M.PROTECT, blank=True, null=True,
                            related_name="exdended_by" )


class AppMixin( Model ):
    class Meta:
        abstract = True
    app = M.ForeignKey( 'App', M.CASCADE )


class Registry( Base, PathMixin ):
    format = JSONField( default=dict )
    default = JSONField( default=dict )
    parent = M.ForeignKey( 'self', M.CASCADE, blank=True, null=True,
                           related_name='_elements' )

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
    def Icon( self ):
        from .objects import Selector
        return Selector( self, Icon )

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

    @property
    def Action( self ):
        from .objects import Selector
        return Selector( self, Action )

    C = Container
    W = Widget
    B = Block
    S = Screen
    H = Shell
    T = Theme
    O = Slot
    A = App
    L = Location
    I = Icon
    K = Link
    R = Reference
    X = Setting
    N = Action

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

    def addicon( self, name, icon ):
        IconEntry.objects.create( registry=self, name=name, entry=icon )

    def addlink( self, name, link ):
        LinkEntry.objects.create( registry=self, name=name, entry=link )

    def addreference( self, name, reference ):
        ReferenceEntry.objects.create( registry=self, name=name, entry=reference )

    def addsetting( self, name, setting ):
        SettingEntry.objects.create( registry=self, name=name, entry=setting )

    def addaction( self, name, action ):
        ActionEntry.objects.create( registry=self, name=name, entry=action )

    def to_dict( self ):
        if not self.active:
            return
        out = super( Registry, self ).to_dict()
        out.update({
            '$default'     : self.default,
            '$format'      : self.format,
        })

        for x in self._container_entries.all():
            out[ x.name ] = x.entry.to_dict()
        for f in '''widget block screen shell theme slot app location
                    link reference setting'''.split():
            data = {}
            for x in getattr( self, "_%s_entries" % f ).all():
                data[ x.name ] = x.entry.to_dict()
            if data:
                out[ "$%ss" % f ] = data
        return out

class Container( Registry ):
    registry_ptr  = M.OneToOneField( Registry, M.CASCADE, parent_link=True,
                                     related_name='_container' )
    registries = M.ManyToManyField( Registry, blank=True, through='ContainerEntry',
                                  related_name='_containers' )


class Widget( Registry, ExtendsMixin, SizeMixin, DataMixin ):
    registry_ptr  = M.OneToOneField( Registry, M.CASCADE, parent_link=True,
                                     related_name='_widget' )
    registries = M.ManyToManyField( Registry, blank=True, through='WidgetEntry',
                                  related_name='_widgets' )


class Block( Registry, ExtendsMixin, SizeMixin, DataMixin ):
    registry_ptr  = M.OneToOneField( Registry, M.CASCADE, parent_link=True,
                                     related_name='_block' )
    registries = M.ManyToManyField( Registry, blank=True, through='BlockEntry',
                                  related_name='_blocks' )


class Screen( Registry, ExtendsMixin, SizeMixin, DataMixin ):
    registry_ptr  = M.OneToOneField( Registry, M.CASCADE, parent_link=True,
                                     related_name='_screen' )
    registries = M.ManyToManyField( Registry, blank=True, through='ScreenEntry',
                                  related_name='_screens' )


class Shell( Registry, ExtendsMixin ):
    registry_ptr  = M.OneToOneField( Registry, M.CASCADE, parent_link=True,
                                     related_name='_shell' )
    registries = M.ManyToManyField( Registry, blank=True, through='ShellEntry',
                                  related_name='_shells' )
    templates = M.CharField( max_length=255 ) # TODO: default
    template = M.CharField( max_length=255, default='index.html' )

    @property
    def home( self ):
        return "%s/%s" % ( self.templates, self.template )

    def to_dict( self ):
        out = super( Link, self).to_dict()
        out.update({
            '$templates' : self.templates,
            '$template' : self.template,
        })
        return out


class Theme( Registry, ExtendsMixin ):
    registry_ptr  = M.OneToOneField( Registry, M.CASCADE, parent_link=True,
                                     related_name='_theme' )
    registries = M.ManyToManyField( Registry, blank=True, through='ThemeEntry',
                                  related_name='_themes' )
    templates = M.CharField( max_length=255 ) # TODO: default
    template = M.CharField( max_length=255, default='index.html' )

    @property
    def home( self ):
        return "%s/%s" % ( self.templates, self.template )

    def to_dict( self ):
        out = super( Link, self).to_dict()
        out.update({
            '$templates' : self.templates,
            '$template' : self.template,
        })
        return out


class Slot( Registry ):
    registry_ptr  = M.OneToOneField( Registry, M.CASCADE, parent_link=True,
                                     related_name='_slot' )
    registries = M.ManyToManyField( Registry, blank=True, through='SlotEntry',
                                  related_name='_slots' )


class App( Registry, DataMixin ):
    registry_ptr  = M.OneToOneField( Registry, M.CASCADE, parent_link=True,
                                     related_name='_app' )
    registries      = M.ManyToManyField( Registry, blank=True, through='AppEntry',
                                       related_name='_apps' )
    module        = M.CharField( max_length=128 )
    rest          = M.CharField( max_length=32, default=True )
    version       = M.CharField( max_length=32, default='0.0.0' )
    available     = M.CharField( max_length=32, default='0.0.0' )

    def to_dict( self ):
        out = super( Link, self).to_dict()
        out.update({
            'module'  : self.module,
            'rest'    : self.rest,
            'version' : self.version,
        })
        return out


class Location( Registry, AppMixin, DataMixin ):
    registries = M.ManyToManyField( Registry, blank=True, through='LocationEntry',
                                  related_name='_locations' )
    href = M.CharField( max_length=255, default='#' )
    redirect_to = M.ForeignKey( 'self', blank=True, null=True,
                                related_name='redirect_from' )

    def to_dict( self ):
        out = super( Location, self).to_dict()
        out.update({
            '$href'        : self.href,
            '$redirect_to' : self.redirect_to.href if self.redirect_to else None
        })
        return out


class Icon( _Base, PathMixin ):
    parent = M.ForeignKey( Registry, M.CASCADE, blank=True, null=True,
                           related_name='_icon_elements' )
    registries = M.ManyToManyField( Registry, blank=True, through='LocationEntry',
                                  related_name='_icons' )


class Link( Base, PathMixin ):
    parent = M.ForeignKey( Registry, M.CASCADE, blank=True, null=True,
                           related_name='_link_elements' )
    registries = M.ManyToManyField( Registry, blank=True, through='LinkEntry',
                                  related_name='links' )
    location = M.ForeignKey( Location, M.SET_NULL, blank=True, null=True,
                             related_name='_links' )

    def to_dict( self ):
        out = super( Link, self).to_dict()
        out.update({
            'location' : self.location.to_dict()
        })
        return out


class Reference( Base, PathMixin ):
    parent = M.ForeignKey( Registry, M.CASCADE, blank=True, null=True,
                           related_name='_registry_elements' )
    registries = M.ManyToManyField( Registry, blank=True, through='ReferenceEntry',
                                  related_name='_references' )
    target = M.CharField( max_length=255 )

    def resolve( self ):
        return Registry.objects.get( name=self.target )
    # TODO: trycatch

    def to_dict( self ):
        out = super( Link, self).to_dict()
        out.update({
            'target' : self.target
        })
        return out


class Setting( Base, PathMixin, DataMixin, ExtendsMixin ):
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
    parent = M.ForeignKey( Registry, M.CASCADE, blank=True, null=True,
                           related_name='_setting_elements' )
    registries = M.ManyToManyField( Registry, blank=True, through='SettingEntry',
                                  related_name='_settings' )
    type     = M.CharField( max_length=32, choices=Types.ALL, default=Types.CHAR )
    default  = JSONField( default=dict )

    def to_dict( self ):
        out = super( Setting, self).to_dict()
        out.update({
            '$type'    : self.type,
            '$default' : self.default
        })
        return out


class Action( Base, PathMixin, DataMixin ):
    parent = M.ForeignKey( Registry, M.CASCADE, blank=True, null=True,
                           related_name='_action_elements' )
    registries = M.ManyToManyField( Registry, blank=True, through='ActionEntry',
                                  related_name='_actions' )


def _get_entry_position():
    return 0

class Entry( Base ):
    class Meta:
        unique_together = ( 'registry', 'name' )
        abstract = True
        verbose_name_plural = 'entries'
    position = M.PositiveSmallIntegerField( default=_get_entry_position )

class ContainerEntry( Entry ):
    class Meta:
        verbose_name_plural = 'container entries'
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_container_entries' )
    entry = M.ForeignKey( Container, M.CASCADE, related_name='_entries' )


class WidgetEntry( Entry, DataMixin ):
    class Meta:
        verbose_name_plural = 'widget entries'
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_widget_entries' )
    entry = M.ForeignKey( Widget, M.CASCADE, related_name='_entries' )


class BlockEntry( Entry, DataMixin ):
    class Meta:
        verbose_name_plural = 'block entries'
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_block_entries' )
    entry = M.ForeignKey( Block, M.CASCADE, related_name='_entries' )


class ScreenEntry( Entry, DataMixin ):
    class Meta:
        verbose_name_plural = 'screen entries'
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_screen_entries' )
    entry = M.ForeignKey( Screen, M.CASCADE, related_name='_entries' )


class ShellEntry( Entry ):
    class Meta:
        verbose_name_plural = 'shell entries'
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_shell_entries' )
    entry = M.ForeignKey( Shell, M.CASCADE, related_name='_entries' )


class ThemeEntry( Entry ):
    class Meta:
        verbose_name_plural = 'theme entries'
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_theme_entries' )
    entry = M.ForeignKey( Theme, M.CASCADE, related_name='_entries' )


class SlotEntry( Entry ):
    class Meta:
        verbose_name_plural = 'slot entries'
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_slot_entries' )
    entry = M.ForeignKey( Slot, M.CASCADE, related_name='_entries' )


class AppEntry( Entry ):
    class Meta:
        verbose_name_plural = 'app entries'
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_app_entries' )
    entry = M.ForeignKey( App, M.CASCADE, related_name='_entries' )


class LocationEntry( Entry ):
    class Meta:
        verbose_name_plural = 'location entries'
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_location_entries' )
    entry = M.ForeignKey( Location, M.CASCADE, related_name='_entries' )


class IconEntry( Entry ):
    class Meta:
        verbose_name_plural = 'icon entries'
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_icon_entries' )
    entry = M.ForeignKey( Icon, M.CASCADE, related_name='_entries' )


class LinkEntry( Entry ):
    class Meta:
        verbose_name_plural = 'link entries'
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_link_entries' )
    entry = M.ForeignKey( Link, M.CASCADE, related_name='_entries' )


class ReferenceEntry( Entry ):
    class Meta:
        verbose_name_plural = 'reference entries'
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_reference_entries' )
    entry = M.ForeignKey( Reference, M.CASCADE, related_name='_entries' )


class SettingEntry( Entry ):
    class Meta:
        verbose_name_plural = 'setting entries'
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_setting_entries' )
    entry = M.ForeignKey( Setting, M.CASCADE, related_name='_entries' )


class ActionEntry( Entry ):
    class Meta:
        verbose_name_plural = 'action entries'
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_action_entries' )
    entry = M.ForeignKey( Action, M.CASCADE, related_name='_entries' )


