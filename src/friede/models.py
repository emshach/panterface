# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models as M
from django.contrib.postgres.fields import JSONField, ArrayField
# from datetime import date
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from model_utils.managers import InheritanceManager
from aries.models import OwnedModel
# from .util import snake_case


Model = M.Model

@python_2_unicode_compatible
class _Base( Model ):
    class Meta:
        abstract = True
    name         = M.SlugField( max_length=255 )
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
        entry, created = self._entries.model.objects.update_or_create(
            registry=self.parent,
            name=self.name,
            defaults=dict( entry=self ))


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


class Registry( OwnedModel, Base, PathMixin ):
    class Meta:
        verbose_name_plural = 'registries'
    app     = M.ForeignKey(
        'App',
        on_delete=M.CASCADE,
        related_name='app_registries',
        null=True,
        blank=True
    )
    format  = JSONField( default=dict )
    default = JSONField( default=dict )
    parent  = M.ForeignKey(
        'self',
        on_delete=M.CASCADE,
        related_name='_elements',
        blank=True,
        null=True
    )

    objects = InheritanceManager()

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

    def addcontainer( self, name, container, defaults={} ):
        return ContainerEntry.objects.update_or_create(
            registry=self, name=name, entry=container, defaults=defaults )

    def addwidget( self, name, widget, defaults={} ):
        return WidgetEntry.objects.update_or_create(
            registry=self, name=name, entry=widget, defaults=defaults )

    def addblock( self, name, block, defaults={} ):
        return BlockEntry.objects.update_or_create(
            registry=self, name=name, entry=block, defaults=defaults )

    def addscreen( self, name, screen, defaults={} ):
        return ScreenEntry.objects.update_or_create(
            registry=self, name=name, entry=screen, defaults=defaults )

    def addshell( self, name, shell, defaults={} ):
        return ShellEntry.objects.update_or_create(
            registry=self, name=name, entry=shell, defaults=defaults )

    def addtheme( self, name, theme, defaults={} ):
        return ThemeEntry.objects.update_or_create(
            registry=self, name=name, entry=theme, defaults=defaults )

    def addslot( self, name, slot, defaults={} ):
        return SlotEntry.objects.update_or_create(
            registry=self, name=name, entry=slot, defaults=defaults )

    def addapp( self, name, app, defaults={} ):
        return AppEntry.objects.update_or_create(
            registry=self, name=name, entry=app, defaults=defaults )

    def addlocation( self, name, location, defaults={} ):
        return LocationEntry.objects.update_or_create(
            registry=self, name=name, entry=location, defaults=defaults )

    def addicon( self, name, icon, defaults={} ):
        return IconEntry.objects.update_or_create(
            registry=self, name=name, entry=icon, defaults=defaults )

    def addlink( self, name, link, defaults={} ):
        return LinkEntry.objects.update_or_create(
            registry=self, name=name, entry=link, defaults=defaults )

    def addreference( self, name, reference, defaults={} ):
        return ReferenceEntry.objects.update_or_create(
            registry=self, name=name, entry=reference, defaults=defaults )

    def addsetting( self, name, setting, defaults={} ):
        return SettingEntry.objects.update_or_create(
            registry=self, name=name, entry=setting, defaults=defaults )

    def addaction( self, name, action, defaults={} ):
        return ActionEntry.objects.update_or_create(
            registry=self, name=name, entry=action, defaults=defaults )

    def to_dict( self ):
        if not self.active:
            return
        out = super( Registry, self ).to_dict()
        out.update({
            '$default' : self.default,
            '$format'  : self.format,
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
    registry_ptr = M.OneToOneField(
        Registry,
        on_delete=M.CASCADE,
        parent_link=True,
        related_name='_container'
    )
    registries   = M.ManyToManyField(
        Registry,
        blank=True,
        through='ContainerEntry',
        related_name='_containers'
    )


class Widget( Registry, ExtendsMixin, SizeMixin, DataMixin ):
    registry_ptr = M.OneToOneField(
        Registry,
        M.CASCADE,
        parent_link=True,
        related_name='_widget'
    )
    registries   = M.ManyToManyField(
        Registry,
        blank=True,
        through='WidgetEntry',
        related_name='_widgets'
    )


class Block( Registry, ExtendsMixin, SizeMixin, DataMixin ):
    registry_ptr = M.OneToOneField(
        Registry,
        on_delete=M.CASCADE,
        parent_link=True,
        related_name='_block'
    )
    registries   = M.ManyToManyField(
        Registry,
        blank=True,
        through='BlockEntry',
        related_name='_blocks'
    )


class Screen( Registry, ExtendsMixin, SizeMixin, DataMixin ):
    registry_ptr = M.OneToOneField(
        Registry,
        on_delete=M.CASCADE,
        parent_link=True,
        related_name='_screen'
    )
    registries   = M.ManyToManyField(
        Registry,
        blank=True,
        through='ScreenEntry',
        related_name='_screens'
    )


class Shell( Registry, ExtendsMixin ):
    registry_ptr = M.OneToOneField(
        Registry,
        on_delete=M.CASCADE,
        parent_link=True,
        related_name='_shell'
    )
    registries   = M.ManyToManyField(
        Registry,
        blank=True,
        through='ShellEntry',
        related_name='_shells'
    )
    templates    = M.CharField( max_length=255 ) # TODO: default
    template     = M.CharField( max_length=255, default='index.html' )

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
    registry_ptr = M.OneToOneField(
        Registry,
        on_delete=M.CASCADE,
        parent_link=True,
        related_name='_theme'
    )
    registries   = M.ManyToManyField(
        Registry,
        blank=True,
        through='ThemeEntry',
        related_name='_themes'
    )
    templates    = M.CharField( max_length=255 ) # TODO: default
    template     = M.CharField( max_length=255, default='index.html' )

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
    registry_ptr = M.OneToOneField(
        Registry,
        on_delete=M.CASCADE,
        parent_link=True,
        related_name='_slot'
    )
    registries   = M.ManyToManyField(
        Registry,
        blank=True,
        through='SlotEntry',
        related_name='_slots'
    )


class App( Registry, DataMixin ):
    registry_ptr      = M.OneToOneField(
        Registry,
        on_delete=M.CASCADE,
        parent_link=True,
        related_name='_app'
    )
    registries        = M.ManyToManyField(
        Registry,
        blank=True,
        through='AppEntry',
        related_name='_apps'
    )
    module            = M.CharField( max_length=128 )
    rest              = M.CharField( max_length=32 ) # TODO: default to name
    installed         = M.BooleanField( default=False )
    version           = M.CharField( max_length=32, default='0.0.0' )
    min_version       = M.CharField( max_length=32, default='0.0.0' )
    available         = M.CharField( max_length=32, default='0.0.0' )
    required          = M.BooleanField( default=False )
    user_required     = M.BooleanField( default=False )
    user_installable  = M.BooleanField( default=True )
    auto_install      = M.BooleanField( default=False )
    auto_user_install = M.BooleanField( default=False )
    users             = M.ManyToManyField(
        get_user_model(),
        blank=True,
        through='UserApp',
        related_name='friede_apps'
    )

    def to_dict( self ):
        out = super( App, self).to_dict()
        out.update({
            '$module'            : self.module,
            '$rest'              : self.rest,
            '$version'           : self.version,
            '$min_version'       : self.min_version,
            '$available'         : self.available,
            '$required'          : self.required,
            '$user_required'     : self.user_required,
            '$user_installable'  : self.user_installable,
            '$auto_install'      : self.auto_install,
            '$auto_user_install' : self.auto_user_install
        })
        return out


class Location( Registry, DataMixin ):
    registry_ptr = M.OneToOneField(
        Registry,
        on_delete=M.CASCADE,
        parent_link=True,
        related_name='_location'
    )
    registries   = M.ManyToManyField(
        Registry,
        blank=True,
        through='LocationEntry',
        related_name='_locations'
    )
    href         = M.CharField( max_length=255, default='#' )
    redirect_to  = M.ForeignKey(
        'self',
        related_name='redirect_from',
        blank=True,
        null=True
    )

    def to_dict( self ):
        out = super( Location, self).to_dict()
        out.update({
            '$href'        : self.href,
            '$redirect_to' : ( self.redirect_to.href
                               if self.redirect_to
                               else None )
        })
        return out


class Icon( _Base, PathMixin ):
    app        = M.ForeignKey(
        'App',
        on_delete=M.CASCADE,
        related_name='app_icons',
        null=True,
        blank=True
    )
    parent     = M.ForeignKey(
        Registry,
        M.CASCADE,
        related_name='_icon_elements',
        blank=True,
        null=True,
    )
    registries = M.ManyToManyField(
        Registry,
        blank=True,
        through='LocationEntry',
        related_name='_icons'
    )


class Link( OwnedModel, Base, PathMixin ):
    app        = M.ForeignKey(
        App,
        on_delete=M.CASCADE,
        related_name='app_links',
        null=True,
        blank=True
    )
    parent     = M.ForeignKey(
        Registry,
        on_delete=M.CASCADE,
        related_name='_link_elements',
        blank=True,
        null=True,
    )
    registries = M.ManyToManyField(
        Registry,
        blank=True,
        through='LinkEntry',
        related_name='links'
    )
    location   = M.ForeignKey(
        Location,
        on_delete=M.SET_NULL,
        related_name='_links',
        blank=True,
        null=True
    )

    def to_dict( self ):
        out = super( Link, self).to_dict()
        out.update({
            'location' : self.location.to_dict()
        })
        return out


class Reference( Base, PathMixin ):
    app        = M.ForeignKey(
        App,
        on_delete=M.CASCADE,
        related_name='app_references',
        null=True,
        blank=True
    )
    parent     = M.ForeignKey(
        Registry,
        on_delete=M.CASCADE,
        related_name='_registry_elements',
        blank=True,
        null=True
    )
    registries = M.ManyToManyField(
        Registry,
        blank=True,
        through='ReferenceEntry',
        related_name='_references'
    )
    target     = M.CharField( max_length=255 )

    def resolve( self ):
        return Registry.objects.get( name=self.target )
    # TODO: trycatch

    def to_dict( self ):
        out = super( Link, self).to_dict()
        out.update({
            'target' : self.target
        })
        return out


class Setting( OwnedModel, Base, PathMixin, DataMixin, ExtendsMixin ):
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
    app        = M.ForeignKey(
        App,
        on_delete=M.CASCADE,
        related_name='app_settings',
        null=True,
        blank=True
    )
    parent     = M.ForeignKey(
        Registry,
        on_delete=M.CASCADE,
        related_name='_setting_elements',
        blank=True,
        null=True
    )
    registries = M.ManyToManyField(
        Registry,
        blank=True,
        through='SettingEntry',
        related_name='_settings'
    )
    type       = M.CharField(
        max_length=32,
        choices=Types.ALL,
        default=Types.CHAR
    )
    default    = JSONField( default=dict )

    def to_dict( self ):
        out = super( Setting, self).to_dict()
        out.update({
            '$type'    : self.type,
            '$default' : self.default
        })
        return out


class Action( OwnedModel, Base, PathMixin, DataMixin ):
    app        = M.ForeignKey(
        App,
        on_delete=M.CASCADE,
        related_name='app_actions',
        null=True,
        blank=True
    )
    parent     = M.ForeignKey(
        Registry,
        on_delete=M.CASCADE,
        related_name='_action_elements',
        blank=True,
        null=True
    )
    registries = M.ManyToManyField(
        Registry,
        blank=True,
        through='ActionEntry',
        related_name='_actions'
    )


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
        unique_together = Entry.Meta.unique_together
        verbose_name_plural = 'container entries'
    registry = M.ForeignKey(
        Registry, M.CASCADE,
        related_name='_container_entries'
    )
    entry    = M.ForeignKey( Container, M.CASCADE, related_name='_entries' )


class WidgetEntry( Entry, DataMixin ):
    class Meta:
        unique_together = Entry.Meta.unique_together
        verbose_name_plural = 'widget entries'
    registry = M.ForeignKey(
        Registry,
        M.CASCADE,
        related_name='_widget_entries'
    )
    entry    = M.ForeignKey( Widget, M.CASCADE, related_name='_entries' )


class BlockEntry( Entry, DataMixin ):
    class Meta:
        unique_together = Entry.Meta.unique_together
        verbose_name_plural = 'block entries'
    registry = M.ForeignKey(
        Registry,
        M.CASCADE,
        related_name='_block_entries'
    )
    entry    = M.ForeignKey( Block, M.CASCADE, related_name='_entries' )


class ScreenEntry( Entry, DataMixin ):
    class Meta:
        unique_together = Entry.Meta.unique_together
        verbose_name_plural = 'screen entries'
    registry = M.ForeignKey(
        Registry,
        M.CASCADE,
        related_name='_screen_entries'
    )
    entry    = M.ForeignKey( Screen, M.CASCADE, related_name='_entries' )


class ShellEntry( Entry ):
    class Meta:
        unique_together = Entry.Meta.unique_together
        verbose_name_plural = 'shell entries'
    registry = M.ForeignKey(
        Registry,
        M.CASCADE,
        related_name='_shell_entries'
    )
    entry    = M.ForeignKey( Shell, M.CASCADE, related_name='_entries' )


class ThemeEntry( Entry ):
    class Meta:
        unique_together = Entry.Meta.unique_together
        verbose_name_plural = 'theme entries'
    registry = M.ForeignKey(
        Registry,
        M.CASCADE,
        related_name='_theme_entries'
    )
    entry    = M.ForeignKey( Theme, M.CASCADE, related_name='_entries' )


class SlotEntry( Entry ):
    class Meta:
        unique_together = Entry.Meta.unique_together
        verbose_name_plural = 'slot entries'
    registry = M.ForeignKey(
        Registry,
        M.CASCADE,
        related_name='_slot_entries'
    )
    entry    = M.ForeignKey( Slot, M.CASCADE, related_name='_entries' )


class AppEntry( Entry ):
    class Meta:
        unique_together = Entry.Meta.unique_together
        verbose_name_plural = 'app entries'
    registry = M.ForeignKey( Registry, M.CASCADE, related_name='_app_entries' )
    entry    = M.ForeignKey( App, M.CASCADE, related_name='_entries' )


class LocationEntry( Entry ):
    class Meta:
        unique_together = Entry.Meta.unique_together
        verbose_name_plural = 'location entries'
    registry = M.ForeignKey(
        Registry,
        M.CASCADE,
        related_name='_location_entries'
    )
    entry    = M.ForeignKey( Location, M.CASCADE, related_name='_entries' )


class IconEntry( Entry ):
    class Meta:
        unique_together = Entry.Meta.unique_together
        verbose_name_plural = 'icon entries'
    registry = M.ForeignKey(
        Registry,
        M.CASCADE,
        related_name='_icon_entries'
    )
    entry    = M.ForeignKey( Icon, M.CASCADE, related_name='_entries' )


class LinkEntry( Entry ):
    class Meta:
        unique_together = Entry.Meta.unique_together
        verbose_name_plural = 'link entries'
    registry = M.ForeignKey(
        Registry,
        M.CASCADE,
        related_name='_link_entries'
    )
    entry    = M.ForeignKey( Link, M.CASCADE, related_name='_entries' )


class ReferenceEntry( Entry ):
    class Meta:
        unique_together = Entry.Meta.unique_together
        verbose_name_plural = 'reference entries'
    registry = M.ForeignKey(
        Registry,
        M.CASCADE,
        related_name='_reference_entries'
    )
    entry    = M.ForeignKey( Reference, M.CASCADE, related_name='_entries' )


class SettingEntry( Entry ):
    class Meta:
        unique_together = Entry.Meta.unique_together
        verbose_name_plural = 'setting entries'
    registry = M.ForeignKey(
        Registry,
        M.CASCADE,
        related_name='_setting_entries'
    )
    entry    = M.ForeignKey( Setting, M.CASCADE, related_name='_entries' )


class ActionEntry( Entry ):
    class Meta:
        unique_together = Entry.Meta.unique_together
        verbose_name_plural = 'action entries'
    registry = M.ForeignKey(
        Registry,
        M.CASCADE,
        related_name='_action_entries'
    )
    entry    = M.ForeignKey( Action, M.CASCADE, related_name='_entries' )


# operatiosn

class _Base( Model ):
    class Meta:
        abstract = True
    name         = M.SlugField( max_length=255 )
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


@python_2_unicode_compatible
class ActionStatus( Model ):
    def __str__( self ):
        return "{}".format( self.name )

    name     = M.SlugField( max_length=255 )
    message  = M.CharField( max_length=255, blank=True, null=True )
    template = M.TextField( blank=True, null=True )
    parent   = M.ForeignKey(
        'self',
        on_delete=M.PROTECT,
        related_name='children',
        blank=True,
        null=True
    )
    goodness = M.FloatField( blank=True, null=True )

    @property
    def value( self ):
        return self.parent.value if self.goodness is None else self.goodness

    def __int__( self ):
        return int( self.value )

    def __float__( self ):
        return self.value

    def __nonzero__( self ):
        return self.value >= 0

    @staticmethod
    def get( name ):
        return ActionStatus.objects.get( name=name )


@python_2_unicode_compatible
class OpStatus( Model ):
    def __str__( self ):
        return "{}".format( self.status.name )
    status    = M.ForeignKey(
        ActionStatus,
        on_delete=M.PROTECT,
        related_name='statuses'
    )
    parent    = M.ForeignKey(
        'self',
        on_delete=M.PROTECT,
        related_name='children',
        blank=True,
        null=True
    )
    message   = M.CharField( max_length=255, blank=True, null=True )
    data      = JSONField( default=dict )
    # dryrun    = M.BooleanField( default=False )
    operation = M.ForeignKey( 'Operation', M.CASCADE, related_name='statuses' )
    time      = M.DateTimeField( default=now )

    def save( self, *args, **kwargs ):
        # if not self.operation.dryrun_ok:
        #     self.dryrun = True
        super( OpStatus, self ).save( *args, **kwargs )
        self.operation.status = self
        self.operation.save()


@python_2_unicode_compatible
class Endorsement( Model ):
    def __str__( self ):
        return "{}".format( self.pk )

    content_type = M.ForeignKey( ContentType, on_delete=M.CASCADE )
    object_id    = M.PositiveIntegerField()
    endorsed     = GenericForeignKey()
    by           = M.CharField( max_length=255 )


@python_2_unicode_compatible
class Operation( Model ):
    def __str__( self ):
        return self.action.path

    user         = M.ForeignKey(
        get_user_model(),
        on_delete=M.CASCADE,
        related_name='friede_operations'
    )
    parent       = M.ForeignKey(
        'self',
        M.PROTECT,
        related_name='children',
        blank=True,
        null=True
    )
    action       = M.ForeignKey(
        Action,
        on_delete=M.SET_NULL,
        related_name='operations',
        blank=True,
        null=True
    )
    hypothetical = M.BooleanField( default=True )
    conflicts    = M.ManyToManyField( 'self' )
    model        = M.ForeignKey(
        ContentType,
        on_delete=M.PROTECT,
        blank=True,
        null=True
    )
    context      = JSONField( default=dict )
    status       = M.ForeignKey(
        OpStatus,
        on_delete=M.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )
    object_id    = M.PositiveIntegerField( blank=True, null=True )
    object_ids   = ArrayField( M.PositiveIntegerField(), default=list )
    ops          = ArrayField(
        JSONField( default=dict ),
        blank=True,
        null=True,
        default=list
    )
    object       = GenericForeignKey( 'model' )
    done         = M.DateTimeField( blank=True, null=True )


@python_2_unicode_compatible
class Question( Model ):
    def __str__( self ):
        return "{}".format( self.name )

    name      = M.SlugField( max_length=255 )
    type      = M.SlugField( max_length=255 )
    data      = JSONField( default=dict )
    operation = M.ForeignKey( Operation, M.CASCADE, related_name='questions' )


# user stuff

@python_2_unicode_compatible
class UserApp( DataMixin ):
    user      = M.ForeignKey(
        get_user_model(),
        on_delete=M.CASCADE,
        related_name='friede_apps_use'
    )
    app       = M.ForeignKey( App, M.CASCADE, related_name='use' )
    installed = M.BooleanField( default=False )
    active    = M.BooleanField( default=False )
    version   = M.CharField( max_length=32, default='0.0.0' )

    def __str__( self ):
        return "{}@{}".format( str( self.app ), str( self.owner ))
