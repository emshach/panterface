# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from .models import *

class ContainerSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Container
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
        )


class WidgetSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Widget
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'extends',
                   'min_x', 'min_y', 'max_x', 'max_y',
                   'data',
        )


class BlockSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Block
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'extends',
                   'min_x', 'min_y', 'max_x', 'max_y',
                   'data',
        )


class ScreenSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Screen
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'extends',
                   'min_x', 'min_y', 'max_x', 'max_y',
                   'data',
                   'data',
        )


class ShellSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Shell
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'extends',
                   'templates', 'template',
        )


class ThemeSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Theme
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'extends',
                   'templates', 'template',
        )


class SlotSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Slot
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
        )


class AppSerializer( serializers.ModelSerializer ):
    class Meta:
        model = App
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'data',
                   'module', 'rest', 'version',
        )


class IconSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Icon
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active',
                   'path',
        )


class LocationSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Location
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'href', 'redirect_to',
        )
LocationSerializer.redirect_to = LocationSerializer()


class LinkSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Link
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'location',
        )


class ReferenceSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Reference
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'target',
        )


class SettingSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Setting
        fields = ( 'url', 'id', 'name', 'title', 'description', 'active', 'icon',
                   'path',
                   'data',
                   'type', 'default',
        )


