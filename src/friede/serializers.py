# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
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
                '_reference_entries', '_setting_entries' )\
                + ( '_containers', '_widgets', '_blocks', '_screens', '_shells',
                    '_themes', '_slots', '_apps', '_locations', '_icons', '_links',
                    '_references', '_settings' )
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


class RegistrySerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    class Meta:
        model = Registry
        fields = F.base + F.entries


class ContainerSerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    class Meta:
        model = Container
        fields = F.base + F.entries


class WidgetSerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    class Meta:
        model = Widget
        fields = F.base + F.entries + F.extends + F.size + F.data


class BlockSerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    class Meta:
        model = Block
        fields = F.base + F.entries + F.extends + F.size + F.data


class ScreenSerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    class Meta:
        model = Screen
        fields = F.base + F.entries + F.extends + F.size + F.data


class ShellSerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    class Meta:
        model = Shell
        fields = F.base + F.entries + F.extends + F.templates + F.data


class ThemeSerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    class Meta:
        model = Theme
        fields = F.base + F.entries + F.extends + F.templates + F.data


class SlotSerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    class Meta:
        model = Slot
        fields = F.base + F.entries


class AppSerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    class Meta:
        model = App
        fields = F.base + F.entries + F.data + F.app


class LocationSerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
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


class ContainerEntrySerializer( ModelSerializer ):
    entry = ContainerSerializer()
    class Meta:
        model = ContainerEntry
        fields = F.entry


class WidgetEntrySerializer( ModelSerializer ):
    entry = WidgetSerializer()
    class Meta:
        model = WidgetEntry
        fields = F.entry


class BlockEntrySerializer( ModelSerializer ):
    entry = BlockSerializer()
    class Meta:
        model = BlockEntry
        fields = F.entry


class ScreenEntrySerializer( ModelSerializer ):
    entry = ScreenSerializer()
    class Meta:
        model = ScreenEntry
        fields = F.entry


class ShellEntrySerializer( ModelSerializer ):
    entry = ShellSerializer()
    class Meta:
        model = ShellEntry
        fields = F.entry


class ThemeEntrySerializer( ModelSerializer ):
    entry = ThemeSerializer()
    class Meta:
        model = ThemeEntry
        fields = F.entry


class SlotEntrySerializer( ModelSerializer ):
    entry = SlotSerializer()
    class Meta:
        model = SlotEntry
        fields = F.entry


class AppEntrySerializer( ModelSerializer ):
    entry = AppSerializer()
    class Meta:
        model = AppEntry
        fields = F.entry


class LocationEntrySerializer( ModelSerializer ):
    entry = LocationSerializer()
    class Meta:
        model = LocationEntry
        fields = F.entry


class IconEntrySerializer( ModelSerializer ):
    entry = IconSerializer()
    class Meta:
        model = IconEntry
        fields = F.entry


class LinkEntrySerializer( ModelSerializer ):
    entry = LinkSerializer()
    class Meta:
        model = LinkEntry
        fields = F.entry


class ReferenceEntrySerializer( ModelSerializer ):
    entry = ReferenceSerializer()
    class Meta:
        model = ReferenceEntry
        fields = F.entry


class SettingEntrySerializer( ModelSerializer ):
    entry = SettingSerializer()
    class Meta:
        model = SettingEntry
        fields = F.entry


for s in ( RegistrySerializer, ContainerSerializer, WidgetEntrySerializer,
           BlockSerializer, ScreenSerializer, ShellSerializer, ThemeSerializer,
           SlotSerializer, AppSerializer, LocationSerializer ):
    if getattr( s.Meta, 'expanded_fields', None ) is None:
        setattr( s.Meta, 'expanded_fields', OrderedDict())
    s.Meta.expanded_fields.update(
        _container_entries=dict(
            serializer=ContainerEntrySerializer,
            id_source='containerentry.registry_id',
            many=True ),
        _widget_entries=dict(
            serializer=WidgetEntrySerializer,
            id_source='widgetentry.registry_id',
            many=True ),
        _block_entries=dict(
            serializer=BlockEntrySerializer,
            id_source='blockentry.registry_id',
            many=True ),
        _screen_entries=dict(
            serializer=ScreenEntrySerializer,
            id_source='screenentry.registry_id',
            many=True ),
        _shell_entries=dict(
            serializer=ShellEntrySerializer,
            id_source='shellentry.registry_id',
            many=True ),
        _theme_entries=dict(
            serializer=ThemeEntrySerializer,
            id_source='themeentry.registry_id',
            many=True ),
        _slot_entries=dict(
            serializer=SlotEntrySerializer,
            id_source='slotentry.registry_id',
            many=True ),
        _app_entries=dict(
            serializer=AppEntrySerializer,
            id_source='appentry.registry_id',
            many=True ),
        _location_entries=dict(
            serializer=LocationEntrySerializer,
            id_source='locationentry.registry_id',
            many=True ),
        _icon_entries=dict(
            serializer=IconEntrySerializer,
            id_source='iconentry.registry_id',
            many=True ),
        _link_entries=dict(
            serializer=LinkEntrySerializer,
            id_source='linkentry.registry_id',
            many=True ),
        _reference_entries=dict(
            serializer=ReferenceEntrySerializer,
            id_source='referenceentry.registry_id',
            many=True ),
        _setting_entries=dict(
            serializer=SettingEntrySerializer,
            id_source='settingentry.registry_id',
            many=True ),
    )

