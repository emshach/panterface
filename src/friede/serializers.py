# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer,\
    HyperlinkedRelatedField, HyperlinkedIdentityField, CharField, SerializerMethodField
from rest_framework_recursive.fields import RecursiveField
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from collections import OrderedDict

from .models import *

class F:
    _base = ( 'url', 'id', 'name', 'title', 'description', 'active', 'path' )
    base = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon', 'path' )
    entries = ( '_container_entries', '_widget_entries', '_block_entries',
                '_screen_entries', '_shell_entries', '_theme_entries', '_slot_entries',
                '_app_entries', '_location_entries', '_icon_entries', '_link_entries',
                '_reference_entries', '_setting_entries' )
    # entries = tuple()
    extends = ( 'extends', )
    size = ( 'min_x', 'min_y', 'max_x', 'max_y' )
    data = ( 'data', )
    templates = ( 'templates', 'template' )
    app = ( 'module', 'rest', 'version' )
    location = ( 'href', 'redirect_to' )
    link = ( 'location', )
    reference = ( 'target', )
    setting = ( 'type', 'default' )
    entry = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon', 'name',
              'entry', 'position' )


class EntrySerializer( ModelSerializer ):
    url = CharField( source='name' )
    registry = SerializerMethodField()
    entry = SerializerMethodField()

    def get_registry( self, instance ):
        return RegistrySerializer( instance.registry ).data

    def get_entry( self, instance ):
        return self.Meta.entry_serializer( instance.registry ).data


class ContainerEntrySerializer( EntrySerializer ):
    class Meta:
        model = ContainerEntry
        fields = F.entry

    def get_entry( self, instance ):
        return self.Meta.ContainerSerializer_serializer( instance.registry ).data


class WidgetEntrySerializer( EntrySerializer ):
    class Meta:
        model = WidgetEntry
        fields = F.entry

    def get_entry( self, instance ):
        return self.Meta.WidgetSerializer( instance.registry ).data


class BlockEntrySerializer( EntrySerializer ):
    class Meta:
        model = BlockEntry
        fields = F.entry

    def get_entry( self, instance ):
        return self.Meta.BlockSerializer( instance.registry ).data


class ScreenEntrySerializer( EntrySerializer ):
    class Meta:
        model = ScreenEntry
        fields = F.entry

    def get_entry( self, instance ):
        return self.Meta.ScreenSerializer( instance.registry ).data


class ShellEntrySerializer( EntrySerializer ):
    class Meta:
        model = ShellEntry
        fields = F.entry

    def get_entry( self, instance ):
        return self.Meta.ShellSerializer( instance.registry ).data


class ThemeEntrySerializer( EntrySerializer ):
    class Meta:
        model = ThemeEntry
        fields = F.entry

    def get_entry( self, instance ):
        return self.Meta.ThemeSerializer( instance.registry ).data


class SlotEntrySerializer( EntrySerializer ):
    class Meta:
        model = SlotEntry
        fields = F.entry

    def get_entry( self, instance ):
        return self.Meta.SlotSerializer( instance.registry ).data


class AppEntrySerializer( EntrySerializer ):
    class Meta:
        model = AppEntry
        fields = F.entry

    def get_entry( self, instance ):
        return self.Meta.AppSerializer( instance.registry ).data


class LocationEntrySerializer( EntrySerializer ):
    class Meta:
        model = LocationEntry
        fields = F.entry

    def get_entry( self, instance ):
        return self.Meta.LocationSerializer( instance.registry ).data


class IconEntrySerializer( EntrySerializer ):
    class Meta:
        model = IconEntry
        fields = F.entry

    def get_entry( self, instance ):
        return self.Meta.IconSerializer( instance.registry ).data


class LinkEntrySerializer( EntrySerializer ):
    class Meta:
        model = LinkEntry
        fields = F.entry

    def get_entry( self, instance ):
        return self.Meta.LinkSerializer( instance.registry ).data


class ReferenceEntrySerializer( EntrySerializer ):
    class Meta:
        model = ReferenceEntry
        fields = F.entry

    def get_entry( self, instance ):
        return self.Meta.ReferenceSerializer( instance.registry ).data


class SettingEntrySerializer( EntrySerializer ):
    class Meta:
        model = SettingEntry
        fields = F.entry

    def get_entry( self, instance ):
        return self.Meta.SettingSerializer( instance.registry ).data


class RegistrySerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    _container_entries = ContainerEntrySerializer( many=True )
    _widget_entries =    WidgetEntrySerializer( many=True )
    _block_entries =     BlockEntrySerializer( many=True )
    _screen_entries =    ScreenEntrySerializer( many=True )
    _shell_entries =     ShellEntrySerializer( many=True )
    _theme_entries =     ThemeEntrySerializer( many=True )
    _slot_entries =      SlotEntrySerializer( many=True )
    _app_entries =       AppEntrySerializer( many=True )
    _location_entries =  LocationEntrySerializer( many=True )
    _icon_entries =      IconEntrySerializer( many=True )
    _link_entries =      LinkEntrySerializer( many=True )
    _reference_entries = ReferenceEntrySerializer( many=True )
    _setting_entries =   SettingEntrySerializer( many=True )
    class Meta:
        model = Registry
        fields = F.base + F.entries


class ContainerSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Container
        fields = F.base + F.entries


class WidgetSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Widget
        fields = F.base + F.entries + F.extends + F.size + F.data


class BlockSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Block
        fields = F.base + F.entries + F.extends + F.size + F.data


class ScreenSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Screen
        fields = F.base + F.entries + F.extends + F.size + F.data


class ShellSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Shell
        fields = F.base + F.entries + F.extends + F.templates


class ThemeSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Theme
        fields = F.base + F.entries + F.extends + F.templates


class SlotSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Slot
        fields = F.base + F.entries


class AppSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = App
        fields = F.base + F.entries + F.data + F.app


class LocationSerializer( HyperlinkedModelSerializer ):
    redirect_to = RecursiveField( allow_null=True )
    class Meta:
        model = Location
        fields = F.base + F.entries + F.data + F.location


class IconSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Icon
        fields = F._base


class LinkSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Link
        fields = F.base + F.entries + F.location


class ReferenceSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Reference
        fields = F.base + F.entries + F.reference


class SettingSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Setting
        fields = F.base + F.data + F.setting


