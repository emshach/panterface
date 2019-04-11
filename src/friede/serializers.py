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
                '_setting_entries' )

    # entries = ( 'containers', 'widgets', 'blocks', 'screens', 'shells',
    #             'themes', 'slots', 'apps', 'locations', 'icons', 'links',
    #             'references', 'settings' )

    registry = ( 'parent', 'format', 'default' )
    extends = ( 'extends', )
    size = ( 'min_x', 'min_y', 'max_x', 'max_y' )
    data = ( 'data', )
    templates = ( 'templates', 'template' )
    app = ( 'module', 'rest', 'version' )
    location = ( 'href', 'redirect_to' )
    link = ( 'location', )
    reference = ( 'target', )
    setting = ( 'type', 'default' )

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


class RegistrySerializer( SerializerExtensionsMixin,
                          IconMixin,
                          HyperlinkedModelSerializer ):
    _container_entries = SerializerMethodField()
    _widget_entries =    SerializerMethodField()
    _block_entries =     SerializerMethodField()
    _screen_entries =    SerializerMethodField()
    _shell_entries =     SerializerMethodField()
    _theme_entries =     SerializerMethodField()
    _slot_entries =      SerializerMethodField()
    _app_entries =       SerializerMethodField()
    _location_entries =  SerializerMethodField()
    _icon_entries =      SerializerMethodField()
    _link_entries =      SerializerMethodField()
    _reference_entries = SerializerMethodField()
    _setting_entries =   SerializerMethodField()

    def get__container_entries( self, obj ):
        if not self.context['view'].detail:
            return
        entry_queryset = obj._container_entries.all()
        return ContainerEntrySerializer(
            entry_queryset, many=True, context=self.context ).data

    def get__widget_entries( self, obj ):
        if not self.context['view'].detail:
            return
        entry_queryset = obj._widget_entries.all()
        return WidgetEntrySerializer(
            entry_queryset, many=True, context=self.context ).data

    def get__block_entries( self, obj ):
        if not self.context['view'].detail:
            return
        entry_queryset = obj._block_entries.all()
        return BlockEntrySerializer(
            entry_queryset, many=True, context=self.context ).data

    def get__screen_entries( self, obj ):
        if not self.context['view'].detail:
            return
        entry_queryset = obj._screen_entries.all()
        return ScreenEntrySerializer(
            entry_queryset, many=True, context=self.context ).data

    def get__shell_entries( self, obj ):
        if not self.context['view'].detail:
            return
        entry_queryset = obj._shell_entries.all()
        return ShellEntrySerializer(
            entry_queryset, many=True, context=self.context ).data

    def get__theme_entries( self, obj ):
        if not self.context['view'].detail:
            return
        entry_queryset = obj._theme_entries.all()
        return ThemeEntrySerializer(
            entry_queryset, many=True, context=self.context ).data

    def get__slot_entries( self, obj ):
        if not self.context['view'].detail:
            return
        entry_queryset = obj._slot_entries.all()
        return SlotEntrySerializer(
            entry_queryset, many=True, context=self.context ).data

    def get__app_entries( self, obj ):
        if not self.context['view'].detail:
            return
        entry_queryset = obj._app_entries.all()
        return AppEntrySerializer(
            entry_queryset, many=True, context=self.context ).data

    def get__location_entries( self, obj ):
        if not self.context['view'].detail:
            return
        entry_queryset = obj._location_entries.all()
        return LocationEntrySerializer(
            entry_queryset, many=True, context=self.context ).data

    def get__icon_entries( self, obj ):
        if not self.context['view'].detail:
            return
        entry_queryset = obj._icon_entries.all()
        return IconEntrySerializer(
            entry_queryset, many=True, context=self.context ).data

    def get__link_entries( self, obj ):
        if not self.context['view'].detail:
            return
        entry_queryset = obj._link_entries.all()
        return LinkEntrySerializer(
            entry_queryset, many=True, context=self.context ).data

    def get__reference_entries( self, obj ):
        if not self.context['view'].detail:
            return
        entry_queryset = obj._reference_entries.all()
        return ReferenceEntrySerializer(
            entry_queryset, many=True, context=self.context ).data

    def get__setting_entries( self, obj ):
        if not self.context['view'].detail:
            return
        entry_queryset = obj._setting_entries.all()
        return SettingEntrySerializer(
            entry_queryset, many=True, context=self.context ).data


    class Meta:
        model = Registry
        fields = F.base + F.registry + F.entries


class ContainerSerializer( RegistrySerializer ):
    class Meta:
        model = Container
        fields = F.base + F.registry + F.entries


class WidgetSerializer( RegistrySerializer, ExtendsMixin ):
    class Meta:
        model = Widget
        fields = F.base + F.registry + F.entries + F.extends + F.size + F.data


class BlockSerializer( RegistrySerializer, ExtendsMixin ):
    class Meta:
        model = Block
        fields = F.base + F.registry + F.entries + F.extends + F.size + F.data


class ScreenSerializer( RegistrySerializer, ExtendsMixin ):
    class Meta:
        model = Screen
        fields = F.base + F.registry + F.entries + F.extends + F.size + F.data


class ShellSerializer( RegistrySerializer, ExtendsMixin ):
    class Meta:
        model = Shell
        fields = F.base + F.registry + F.entries + F.extends + F.templates


class ThemeSerializer( RegistrySerializer, ExtendsMixin ):
    class Meta:
        model = Theme
        fields = F.base + F.registry + F.entries + F.extends + F.templates


class SlotSerializer( RegistrySerializer ):
    class Meta:
        model = Slot
        fields = F.base + F.registry + F.entries


class AppSerializer( RegistrySerializer ):
    class Meta:
        model = App
        fields = F.base + F.registry + F.entries + F.data + F.app


class LocationSerializer( RegistrySerializer ):
    redirect_to = RecursiveField( allow_null=True, data=None )
    class Meta:
        model = Location
        fields = F.base + F.registry + F.entries + F.data + F.location


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


class EntrySerializer( ModelSerializer, IconMixin ):
    url = CharField( source='name' )
    registry = RegistrySerializer()


class ContainerEntrySerializer( EntrySerializer ):
    entry = ContainerSerializer()
    class Meta:
        model = ContainerEntry
        fields = F.entry


class WidgetEntrySerializer( EntrySerializer ):
    entry = WidgetSerializer()
    class Meta:
        model = WidgetEntry
        fields = F.entry


class BlockEntrySerializer( EntrySerializer ):
    entry = BlockSerializer()
    class Meta:
        model = BlockEntry
        fields = F.entry


class ScreenEntrySerializer( EntrySerializer ):
    entry = ScreenSerializer()
    class Meta:
        model = ScreenEntry
        fields = F.entry


class ShellEntrySerializer( EntrySerializer ):
    entry = ShellSerializer()
    class Meta:
        model = ShellEntry
        fields = F.entry


class ThemeEntrySerializer( EntrySerializer ):
    entry = ThemeSerializer()
    class Meta:
        model = ThemeEntry
        fields = F.entry


class SlotEntrySerializer( EntrySerializer ):
    entry = SlotSerializer()
    class Meta:
        model = SlotEntry
        fields = F.entry


class AppEntrySerializer( EntrySerializer ):
    entry = AppSerializer()
    class Meta:
        model = AppEntry
        fields = F.entry


class LocationEntrySerializer( EntrySerializer ):
    entry = LocationSerializer()
    class Meta:
        model = LocationEntry
        fields = F.entry


class IconEntrySerializer( EntrySerializer ):
    entry = IconSerializer()
    class Meta:
        model = IconEntry
        fields = F.entry


class LinkEntrySerializer( EntrySerializer ):
    entry = LinkSerializer()
    class Meta:
        model = LinkEntry
        fields = F.entry


class ReferenceEntrySerializer( EntrySerializer ):
    entry = ReferenceSerializer()
    class Meta:
        model = ReferenceEntry
        fields = F.entry


class SettingEntrySerializer( EntrySerializer ):
    entry = SettingSerializer()
    class Meta:
        model = SettingEntry
        fields = F.entry


