# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.serializers import (
    Serializer, ModelSerializer, HyperlinkedModelSerializer, HyperlinkedRelatedField,
    HyperlinkedIdentityField, CharField, SerializerMethodField
)
from rest_framework_recursive.fields import RecursiveField
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from collections import OrderedDict

from .models import *

class F:
    _base = ( 'url', 'id', 'name', 'title', 'description', 'active', 'path' )
    base = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon', 'path' )

    entries = ( '_container_entries', '_widget_entries', '_block_entries',
                '_screen_entries', '_shell_entries', '_theme_entries',
                '_slot_entries', '_app_entries', '_location_entries',
                '_icon_entries', '_link_entries', '_reference_entries',
                '_setting_entries', '_action_entries' )

    # entries = ( 'containers', 'widgets', 'blocks', 'screens', 'shells',
    #             'themes', 'slots', 'apps', 'locations', 'icons', 'links',
    #             'references', 'settings', 'actions' )

    registry = ( 'parent', 'format', 'default' )
    extends = ( 'extends', )
    size = ( 'min_x', 'min_y', 'max_x', 'max_y' )
    data = ( 'data', )
    templates = ( 'templates', 'template' )
    app = ( 'module', 'rest', 'installed', 'version', 'min_version', 'available',
            'required', 'user_required', 'user_installable', 'auto_install',
            'auto_user_install' )
    location = ( 'href', 'redirect_to' )
    link = ( 'location', )
    reference = ( 'target', )
    setting = ( 'type', 'default' )
    action = ( 'data', )

    entry = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
              'name', 'entry', 'position' )


class ExtendsMixin( Serializer ):
    extends = RecursiveField( allow_null=True, data=None )


class IconSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Icon
        fields = F._base


class IconMixin( Serializer ):
    icon = IconSerializer()


class EntrySerializer( ModelSerializer, IconMixin ):
    url = CharField( source='name' )
    entry = SerializerMethodField()

    def get_entry( self, obj ):
        return RegistrySerializer( obj.entry ).data


class ContainerEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return ContainerSerializer( obj.entry, context=self.context ).data
    class Meta:
        model = ContainerEntry
        fields = F.entry


class WidgetEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return WidgetSerializer( obj.entry, context=self.context ).data
    class Meta:
        model = WidgetEntry
        fields = F.entry + F.data


class BlockEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return BlockSerializer( obj.entry, context=self.context ).data
    class Meta:
        model = BlockEntry
        fields = F.entry + F.data


class ScreenEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return ScreenSerializer( obj.entry, context=self.context ).data
    class Meta:
        model = ScreenEntry
        fields = F.entry + F.data


class ShellEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return ShellSerializer( obj.entry, context=self.context ).data
    class Meta:
        model = ShellEntry
        fields = F.entry


class ThemeEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return ThemeSerializer( obj.entry, context=self.context ).data
    class Meta:
        model = ThemeEntry
        fields = F.entry


class SlotEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return SlotSerializer( obj.entry, context=self.context ).data
    class Meta:
        model = SlotEntry
        fields = F.entry


class AppEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return AppSerializer( obj.entry, context=self.context ).data
    class Meta:
        model = AppEntry
        fields = F.entry


class LocationEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return LocationSerializer( obj.entry, context=self.context ).data
    class Meta:
        model = LocationEntry
        fields = F.entry


class IconEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return IconSerializer( obj.entry, context=self.context ).data
    class Meta:
        model = IconEntry
        fields = F.entry


class LinkEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return LinkSerializer( obj.entry, context=self.context ).data
    class Meta:
        model = LinkEntry
        fields = F.entry


class ReferenceEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return ReferenceSerializer( obj.entry, context=self.context ).data
    class Meta:
        model = ReferenceEntry
        fields = F.entry


class SettingEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return SettingSerializer( obj.entry, context=self.context ).data
    class Meta:
        model = SettingEntry
        fields = F.entry


class ActionEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return ActionSerializer( obj.entry, context=self.context ).data
    class Meta:
        model = ActionEntry
        fields = F.entry


class RegistrySerializer( SerializerExtensionsMixin,
                          IconMixin,
                          HyperlinkedModelSerializer ):

    class Meta:
        model = Registry
        fields = F.base + F.registry # + F.entries
        expandable_fields=OrderedDict(
            _container_entries=dict(
                serializer=ContainerEntrySerializer,
                id_source=False,
                many=True ),
            _widget_entries=dict(
                serializer=WidgetEntrySerializer,
                id_source=False,
                many=True ),
            _block_entries=dict(
                serializer=BlockEntrySerializer,
                id_source=False,
                many=True ),
            _screen_entries=dict(
                serializer=ScreenEntrySerializer,
                id_source=False,
                many=True ),
            _shell_entries=dict(
                serializer=ShellEntrySerializer,
                id_source=False,
                many=True ),
            _theme_entries=dict(
                serializer=ThemeEntrySerializer,
                id_source=False,
                many=True ),
            _slot_entries=dict(
                serializer=SlotEntrySerializer,
                id_source=False,
                many=True ),
            _app_entries=dict(
                serializer=AppEntrySerializer,
                id_source=False,
                many=True ),
            _location_entries=dict(
                serializer=LocationEntrySerializer,
                id_source=False,
                many=True ),
            _icon_entries=dict(
                serializer=IconEntrySerializer,
                id_source=False,
                many=True ),
            _link_entries=dict(
                serializer=LinkEntrySerializer,
                id_source=False,
                many=True ),
            _reference_entries=dict(
                serializer=ReferenceEntrySerializer,
                id_source=False,
                many=True ),
            _setting_entries=dict(
                serializer=SettingEntrySerializer,
                id_source=False,
                many=True ),
            _action_entries=dict(
                serializer=ActionEntrySerializer,
                id_source=False,
                many=True ),
        )


class ContainerSerializer( RegistrySerializer ):
    class Meta:
        model = Container
        fields = RegistrySerializer.Meta.fields
        expandable_fields = RegistrySerializer.Meta.expandable_fields


class WidgetSerializer( RegistrySerializer ):
    extends = RecursiveField( allow_null=True, data=None )
    class Meta:
        model = Widget
        fields = RegistrySerializer.Meta.fields + F.extends + F.size + F.data
        expandable_fields = RegistrySerializer.Meta.expandable_fields


class BlockSerializer( RegistrySerializer, ExtendsMixin ):
    class Meta:
        model = Block
        fields = RegistrySerializer.Meta.fields + F.extends + F.size + F.data
        expandable_fields = RegistrySerializer.Meta.expandable_fields


class ScreenSerializer( RegistrySerializer, ExtendsMixin ):
    class Meta:
        model = Screen
        fields = RegistrySerializer.Meta.fields + F.extends + F.size + F.data
        expandable_fields = RegistrySerializer.Meta.expandable_fields


class ShellSerializer( RegistrySerializer, ExtendsMixin ):
    class Meta:
        model = Shell
        fields = RegistrySerializer.Meta.fields + F.extends + F.templates
        expandable_fields = RegistrySerializer.Meta.expandable_fields


class ThemeSerializer( RegistrySerializer, ExtendsMixin ):
    class Meta:
        model = Theme
        fields = RegistrySerializer.Meta.fields + F.extends + F.templates
        expandable_fields = RegistrySerializer.Meta.expandable_fields


class SlotSerializer( RegistrySerializer ):
    class Meta:
        model = Slot
        fields = RegistrySerializer.Meta.fields
        expandable_fields = RegistrySerializer.Meta.expandable_fields


class AppSerializer( RegistrySerializer ):
    class Meta:
        model = App
        fields = RegistrySerializer.Meta.fields + F.data + F.app
        expandable_fields = RegistrySerializer.Meta.expandable_fields


class LocationSerializer( RegistrySerializer ):
    redirect_to = RecursiveField( allow_null=True, data=None )
    class Meta:
        model = Location
        fields = RegistrySerializer.Meta.fields + F.data + F.location
        expandable_fields = RegistrySerializer.Meta.expandable_fields


class LinkSerializer( HyperlinkedModelSerializer, IconMixin ):
    class Meta:
        model = Link
        fields = F.base + F.link
        expandable_fields = RegistrySerializer.Meta.expandable_fields


class ReferenceSerializer( HyperlinkedModelSerializer, IconMixin ):
    class Meta:
        model = Reference
        fields = F.base + F.reference
        expandable_fields = RegistrySerializer.Meta.expandable_fields


class SettingSerializer( HyperlinkedModelSerializer, IconMixin ):
    class Meta:
        model = Setting
        fields = F.base + F.setting
        expandable_fields = RegistrySerializer.Meta.expandable_fields


class ActionSerializer( HyperlinkedModelSerializer, IconMixin ):
    class Meta:
        model = Action
        fields = F.base + F.action
        expandable_fields = RegistrySerializer.Meta.expandable_fields


by_model = dict(
    registry=  RegistrySerializer,
    container= ContainerSerializer,
    widget=    WidgetSerializer,
    block=     BlockSerializer,
    screen=    ScreenSerializer,
    shell=     ShellSerializer,
    theme=     ThemeSerializer,
    slot=      SlotSerializer,
    app=       AppSerializer,
    location=  LocationSerializer,
    link=      LinkSerializer,
    reference= ReferenceSerializer,
    setting=   SettingSerializer,
    action=    ActionSerializer,
    containerentry= ContainerEntrySerializer,
    widgetentry=    WidgetEntrySerializer,
    blockentry=     BlockEntrySerializer,
    screenentry=    ScreenEntrySerializer,
    shellentry=     ShellEntrySerializer,
    themeentry=     ThemeEntrySerializer,
    slotentry=      SlotEntrySerializer,
    appentry=       AppEntrySerializer,
    locationentry=  LocationEntrySerializer,
    linkentry=      LinkEntrySerializer,
    referenceentry= ReferenceEntrySerializer,
    settingentry=   SettingEntrySerializer,
    actionentry=    ActionEntrySerializer,
)
