# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from rest_framework_recursive.fields import RecursiveField
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from collections import OrderedDict

from .models import *

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
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'href', 'redirect_to'
        )


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


for s in ( ContainerSerializer, WidgetEntrySerializer, BlockSerializer,
           ScreenSerializer, ShellSerializer, ThemeSerializer, SlotSerializer,
           AppSerializer, LocationSerializer ):
    if getattr( s.Meta, 'expanded_fields', None ) is None:
        setattr( s.Meta, 'expanded_fields', OrderedDict())
    s.expanded_fields.update(
        containers=dict(
            serializer=ContainerEntrySerializer,
            many=True ),
        widgets=dict(
            serializer=WidgetEntrySerializer,
            many=True ),
        blocks=dict(
            serializer=BlockEntrySerializer,
            many=True ),
        screens=dict(
            serializer=ScreenEntrySerializer,
            many=True ),
        shells=dict(
            serializer=ShellEntrySerializer,
            many=True ),
        themes=dict(
            serializer=ThemeEntrySerializer,
            many=True ),
        slots=dict(
            serializer=SlotEntrySerializer,
            many=True ),
        apps=dict(
            serializer=AppEntrySerializer,
            many=True ),
        locations=dict(
            serializer=LocationEntrySerializer,
            many=True ),
        icons=dict(
            serializer=IconEntrySerializer,
            many=True ),
        links=dict(
            serializer=LinkEntrySerializer,
            many=True ),
        references=dict(
            serializer=ReferenceEntrySerializer,
            many=True ),
        settings=dict(
            serializer=SettingEntrySerializer,
            many=True ),
    )

