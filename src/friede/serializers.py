# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from .models import *

class ContainerSerializer( serializers.HyperlinkedModelSerializer ):
    class Meta:
        model = Container
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
        )


class WidgetSerializer( serializers.HyperlinkedModelSerializer ):
    class Meta:
        model = Widget
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'extends',
                   'min_x', 'min_y', 'max_x', 'max_y',
                   'data',
        )


class WidgetEntrySerializer( serializers.HyperlinkedModelSerializer ):
    entry = WidgetSerializer()
    class Meta:
        model = WidgetEntry
        fields = ( 'name', 'entry' )


class BlockSerializer( serializers.HyperlinkedModelSerializer ):
    class Meta:
        model = Block
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'extends',
                   'min_x', 'min_y', 'max_x', 'max_y',
                   'data',
        )


class ScreenSerializer( serializers.HyperlinkedModelSerializer ):
    class Meta:
        model = Screen
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'extends',
                   'min_x', 'min_y', 'max_x', 'max_y',
                   'data',
                   'data',
        )


class ShellSerializer( serializers.HyperlinkedModelSerializer ):
    class Meta:
        model = Shell
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'extends',
                   'templates', 'template',
        )


class ThemeSerializer( serializers.HyperlinkedModelSerializer ):
    class Meta:
        model = Theme
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'extends',
                   'templates', 'template',
        )


class SlotSerializer( serializers.HyperlinkedModelSerializer ):
    class Meta:
        model = Slot
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
        )


class AppSerializer( serializers.HyperlinkedModelSerializer ):
    class Meta:
        model = App
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'data',
                   'module', 'rest', 'version',
        )


class IconSerializer( serializers.HyperlinkedModelSerializer ):
    class Meta:
        model = Icon
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active',
                   'path',
        )


class LocationSerializer( serializers.HyperlinkedModelSerializer ):
    redirect_to = RecursiveField( allow_null=True )
    _widget_entries = WidgetEntrySerializer()
    class Meta:
        model = Location
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'href', 'redirect_to',
                   '_widget_entries'
        )


class LinkSerializer( serializers.HyperlinkedModelSerializer ):
    class Meta:
        model = Link
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'location',
        )


class ReferenceSerializer( serializers.HyperlinkedModelSerializer ):
    class Meta:
        model = Reference
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'target',
        )


class SettingSerializer( serializers.HyperlinkedModelSerializer ):
    class Meta:
        model = Setting
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'data',
                   'type', 'default',
        )


