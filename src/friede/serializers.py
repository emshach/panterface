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

    # entries = ( '_container_entries', '_widget_entries', '_block_entries',
    #             '_screen_entries', '_shell_entries', '_theme_entries',
    #             '_slot_entries', '_app_entries', '_location_entries',
    #             '_icon_entries', '_link_entries', '_reference_entries',
    #             '_setting_entries' )

    entries = ( 'containers', 'widgets', 'blocks', 'screens', 'shells',
                'themes', 'slots', 'apps', 'locations', 'icons', 'links',
                'references', 'settings' )

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


class RegistrySerializer( SerializerExtensionsMixin, HyperlinkedModelSerializer ):
    containers = SerializerMethodField()
    widgets =    SerializerMethodField()
    blocks =     SerializerMethodField()
    screens =    SerializerMethodField()
    shells =     SerializerMethodField()
    themes =     SerializerMethodField()
    slots =      SerializerMethodField()
    apps =       SerializerMethodField()
    locations =  SerializerMethodField()
    icons =      SerializerMethodField()
    links =      SerializerMethodField()
    references = SerializerMethodField()
    settings =   SerializerMethodField()

    def get_containers( self, obj ):
        entry_queryset = obj._container_entries.all()
        ContainerEntrySerializer( entry_queryset, many=True ).data

    def get_widgets( self, obj ):
        entry_queryset = obj._widget_entries.all()
        WidgetEntrySerializer( entry_queryset, many=True ).data

    def get_blocks( self, obj ):
        entry_queryset = obj._block_entries.all()
        BlockEntrySerializer( entry_queryset, many=True ).data

    def get_screens( self, obj ):
        entry_queryset = obj._screen_entries.all()
        ScreenEntrySerializer( entry_queryset, many=True ).data

    def get_shells( self, obj ):
        entry_queryset = obj._shell_entries.all()
        return ShellEntrySerializer( entry_queryset, many=True ).data

    def get_themes( self, obj ):
        entry_queryset = obj._theme_entries.all()
        ThemeEntrySerializer( entry_queryset, many=True ).data

    def get_slots( self, obj ):
        entry_queryset = obj._slot_entries.all()
        SlotEntrySerializer( entry_queryset, many=True ).data

    def get_apps( self, obj ):
        entry_queryset = obj._app_entries.all()
        AppEntrySerializer( entry_queryset, many=True ).data

    def get_locations( self, obj ):
        entry_queryset = obj._location_entries.all()
        LocationEntrySerializer( entry_queryset, many=True ).data

    def get_icons( self, obj ):
        entry_queryset = obj._icon_entries.all()
        IconEntrySerializer( entry_queryset, many=True ).data

    def get_links( self, obj ):
        entry_queryset = obj._link_entries.all()
        LinkEntrySerializer( entry_queryset, many=True ).data

    def get_references( self, obj ):
        entry_queryset = obj._reference_entries.all()
        ReferenceEntrySerializer( entry_queryset, many=True ).data

    def get_settings( self, obj ):
        entry_queryset = obj._setting_entries.all()
        SettingEntrySerializer( entry_queryset, many=True ).data


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


class EntrySerializer( ModelSerializer ):
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


