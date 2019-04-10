# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from rest_framework_recursive.fields import RecursiveField
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from collections import OrderedDict

from .models import *

class RegistrySerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    class Meta:
        model = Registry
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   '_container_entries',
        )


class ContainerSerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    class Meta:
        model = Container
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
        )


class WidgetSerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    class Meta:
        model = Widget
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'extends',
                   'min_x', 'min_y', 'max_x', 'max_y',
                   'data',
        )


class BlockSerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    class Meta:
        model = Block
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'extends',
                   'min_x', 'min_y', 'max_x', 'max_y',
                   'data',
        )


class ScreenSerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    class Meta:
        model = Screen
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'extends',
                   'min_x', 'min_y', 'max_x', 'max_y',
                   'data',
                   'data',
        )


class ShellSerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    class Meta:
        model = Shell
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'extends',
                   'templates', 'template',
        )


class ThemeSerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    class Meta:
        model = Theme
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'extends',
                   'templates', 'template',
        )


class SlotSerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    class Meta:
        model = Slot
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
        )


class AppSerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    class Meta:
        model = App
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'data',
                   'module', 'rest', 'version',
        )


class LocationSerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    redirect_to = RecursiveField( allow_null=True )
    class Meta:
        model = Location
        fields = '__all__'


class IconSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Icon
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active',
                   'path',
        )


class LinkSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Link
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'location',
        )


class ReferenceSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Reference
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'target',
        )


class SettingSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Setting
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'data',
                   'type', 'default',
        )


class ContainerEntrySerializer( ModelSerializer ):
    entry = ContainerSerializer()
    class Meta:
        model = ContainerEntry
        fields = ( 'name', 'entry' )


class WidgetEntrySerializer( ModelSerializer ):
    entry = WidgetSerializer()
    class Meta:
        model = WidgetEntry
        fields = ( 'name', 'entry' )


class BlockEntrySerializer( ModelSerializer ):
    entry = BlockSerializer()
    class Meta:
        model = BlockEntry
        fields = ( 'name', 'entry' )


class ScreenEntrySerializer( ModelSerializer ):
    entry = ScreenSerializer()
    class Meta:
        model = ScreenEntry
        fields = ( 'name', 'entry' )


class ShellEntrySerializer( ModelSerializer ):
    entry = ShellSerializer()
    class Meta:
        model = ShellEntry
        fields = ( 'name', 'entry' )


class ThemeEntrySerializer( ModelSerializer ):
    entry = ThemeSerializer()
    class Meta:
        model = ThemeEntry
        fields = ( 'name', 'entry' )


class SlotEntrySerializer( ModelSerializer ):
    entry = SlotSerializer()
    class Meta:
        model = SlotEntry
        fields = ( 'name', 'entry' )


class AppEntrySerializer( ModelSerializer ):
    entry = AppSerializer()
    class Meta:
        model = AppEntry
        fields = ( 'name', 'entry' )


class LocationEntrySerializer( ModelSerializer ):
    entry = LocationSerializer()
    class Meta:
        model = LocationEntry
        fields = ( 'name', 'entry' )


class IconEntrySerializer( ModelSerializer ):
    entry = IconSerializer()
    class Meta:
        model = IconEntry
        fields = ( 'name', 'entry' )


class LinkEntrySerializer( ModelSerializer ):
    entry = LinkSerializer()
    class Meta:
        model = LinkEntry
        fields = ( 'name', 'entry' )


class ReferenceEntrySerializer( ModelSerializer ):
    entry = ReferenceSerializer()
    class Meta:
        model = ReferenceEntry
        fields = ( 'name', 'entry' )


class SettingEntrySerializer( ModelSerializer ):
    entry = SettingSerializer()
    class Meta:
        model = SettingEntry
        fields = ( 'name', 'entry' )


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

