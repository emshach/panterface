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


class EntrySerializer( ModelSerializer, IconMixin ):
    url = CharField( source='name' )
    registry = RegistrySerializer()
    entry = SerializerMethodField()


class ContainerEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return ContainerSerializer( obj.entry ).data
    class Meta:
        model = ContainerEntry
        fields = F.entry


class WidgetEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return WidgetSerializer( obj.entry ).data
    class Meta:
        model = WidgetEntry
        fields = F.entry


class BlockEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return BlockSerializer( obj.entry ).data
    class Meta:
        model = BlockEntry
        fields = F.entry


class ScreenEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return ScreenSerializer( obj.entry ).data
    class Meta:
        model = ScreenEntry
        fields = F.entry


class ShellEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return ShellSerializer( obj.entry ).data
    class Meta:
        model = ShellEntry
        fields = F.entry


class ThemeEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return ThemeSerializer( obj.entry ).data
    class Meta:
        model = ThemeEntry
        fields = F.entry


class SlotEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return SlotSerializer( obj.entry ).data
    class Meta:
        model = SlotEntry
        fields = F.entry


class AppEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return AppSerializer( obj.entry ).data
    class Meta:
        model = AppEntry
        fields = F.entry


class LocationEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return LocationSerializer( obj.entry ).data
    class Meta:
        model = LocationEntry
        fields = F.entry


class IconEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return IconSerializer( obj.entry ).data
    class Meta:
        model = IconEntry
        fields = F.entry


class LinkEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return LinkSerializer( obj.entry ).data
    class Meta:
        model = LinkEntry
        fields = F.entry


class ReferenceEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return ReferenceSerializer( obj.entry ).data
    class Meta:
        model = ReferenceEntry
        fields = F.entry


class SettingEntrySerializer( EntrySerializer ):
    def get_entry( self, obj ):
        return SettingSerializer( obj.entry ).data
    class Meta:
        model = SettingEntry
        fields = F.entry


class RegistrySerializer( SerializerExtensionsMixin,
                          IconMixin,
                          HyperlinkedModelSerializer ):

    class Meta:
        model = Registry
        fields = F.base + F.registry + F.entries
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
        )

    # _container_entries = SerializerMethodField()
    # _widget_entries =    SerializerMethodField()
    # _block_entries =     SerializerMethodField()
    # _screen_entries =    SerializerMethodField()
    # _shell_entries =     SerializerMethodField()
    # _theme_entries =     SerializerMethodField()
    # _slot_entries =      SerializerMethodField()
    # _app_entries =       SerializerMethodField()
    # _location_entries =  SerializerMethodField()
    # _icon_entries =      SerializerMethodField()
    # _link_entries =      SerializerMethodField()
    # _reference_entries = SerializerMethodField()
    # _setting_entries =   SerializerMethodField()

    # def get__container_entries( self, obj ):
    #     if not self.context.get( 'detail' ) and not self.context['view'].detail:
    #         return
    #     entry_queryset = obj._container_entries.all()
    #     return ContainerEntrySerializer(
    #         entry_queryset, many=True, context=self.context ).data

    # def get__widget_entries( self, obj ):
    #     if not self.context.get( 'detail' ) and not self.context['view'].detail:
    #         return
    #     entry_queryset = obj._widget_entries.all()
    #     return WidgetEntrySerializer(
    #         entry_queryset, many=True, context=self.context ).data

    # def get__block_entries( self, obj ):
    #     if not self.context.get( 'detail' ) and not self.context['view'].detail:
    #         return
    #     entry_queryset = obj._block_entries.all()
    #     return BlockEntrySerializer(
    #         entry_queryset, many=True, context=self.context ).data

    # def get__screen_entries( self, obj ):
    #     if not self.context.get( 'detail' ) and not self.context['view'].detail:
    #         return
    #     entry_queryset = obj._screen_entries.all()
    #     return ScreenEntrySerializer(
    #         entry_queryset, many=True, context=self.context ).data

    # def get__shell_entries( self, obj ):
    #     if not self.context.get( 'detail' ) and not self.context['view'].detail:
    #         return
    #     entry_queryset = obj._shell_entries.all()
    #     return ShellEntrySerializer(
    #         entry_queryset, many=True, context=self.context ).data

    # def get__theme_entries( self, obj ):
    #     if not self.context.get( 'detail' ) and not self.context['view'].detail:
    #         return
    #     entry_queryset = obj._theme_entries.all()
    #     return ThemeEntrySerializer(
    #         entry_queryset, many=True, context=self.context ).data

    # def get__slot_entries( self, obj ):
    #     if not self.context.get( 'detail' ) and not self.context['view'].detail:
    #         return
    #     entry_queryset = obj._slot_entries.all()
    #     return SlotEntrySerializer(
    #         entry_queryset, many=True, context=self.context ).data

    # def get__app_entries( self, obj ):
    #     if not self.context.get( 'detail' ) and not self.context['view'].detail:
    #         return
    #     entry_queryset = obj._app_entries.all()
    #     return AppEntrySerializer(
    #         entry_queryset, many=True, context=self.context ).data

    # def get__location_entries( self, obj ):
    #     if not self.context.get( 'detail' ) and not self.context['view'].detail:
    #         return
    #     entry_queryset = obj._location_entries.all()
    #     return LocationEntrySerializer(
    #         entry_queryset, many=True, context=self.context ).data

    # def get__icon_entries( self, obj ):
    #     if not self.context.get( 'detail' ) and not self.context['view'].detail:
    #         return
    #     entry_queryset = obj._icon_entries.all()
    #     return IconEntrySerializer(
    #         entry_queryset, many=True, context=self.context ).data

    # def get__link_entries( self, obj ):
    #     if not self.context.get( 'detail' ) and not self.context['view'].detail:
    #         return
    #     entry_queryset = obj._link_entries.all()
    #     return LinkEntrySerializer(
    #         entry_queryset, many=True, context=self.context ).data

    # def get__reference_entries( self, obj ):
    #     if not self.context.get( 'detail' ) and not self.context['view'].detail:
    #         return
    #     entry_queryset = obj._reference_entries.all()
    #     return ReferenceEntrySerializer(
    #         entry_queryset, many=True, context=self.context ).data

    # def get__setting_entries( self, obj ):
    #     if not self.context.get( 'detail' ) and not self.context['view'].detail:
    #         return
    #     entry_queryset = obj._setting_entries.all()
    #     return SettingEntrySerializer(
    #         entry_queryset, many=True, context=self.context ).data


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


