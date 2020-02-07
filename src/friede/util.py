# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from packaging.version import parse as version_parse, _BaseVersion
from django.contrib.contenttypes.models import ContentType
from django.db.models.base import Model as BaseModel
import re


def snake_case( str ):
    return re.sub(r'(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', r'_\1', str )\
             .lower().strip('_')


def split_dict( obj, *keys ):
    d1 = {}
    d2 = {}
    for key, value in obj.items():
        ( d1 if key in keys else d2 )[ key ] = value
    return d1, d2


def as_tree( col, field='path', sep='.' ):
    tree = {}
    for item in col:
        node = tree
        path = getattr( item, field ).split( sep )
        while path and not path[-1]:
            path.pop()
        for x in path:
            if not x:
                continue
            if x not in node:
                node[x] = {}
            node = node[x]
        node['$'] = item.to_dict()
    return tree


def toversion( version ):
    if isinstance( version, _BaseVersion ):
        return version
    return version_parse( version )


form_field_mappings = dict(
    AutoField=None,
    BigAutoField=None,
    BigIntegerField='IntegerField',
    CommaSeparatedIntegerField='CharField',
    ForeignKey='ModelChoiceField',
    GenericIPAddressField='GenericIpAddressField',
    IPAddressField='IpAddressField',
    JSONField='JsonField',
    OneToOneRel='ModelChoiceField',
    OneToOneField='ModelChoiceField',
    ManyToManyField='ModelMultipleChoiceField',
    ManyToManyRel='ModelMultipleChoiceField',
    ManyToOneRel='ModelMultipleChoiceField',
    PositiveIntegerField='IntegerField',
    PositiveSmallIntegerField='IntegerField',
    SmallIntegerField='IntegerField',
    URLField='UrlField',
    UUIDField='UuidField',
)


class Noop( object ):
    def __getattribute__( self, name ):
        return None


def getmodel( name, app=None ):
    if isinstance( name, BaseModel ):
        return name.__class__
    try:
        if issubclass( name, BaseModel ):
            return name
    except TypeError:
        pass
    app, model = ( app, name ) if app else name.split('.')
    try:
        obj = ContentType.objects.get( app_label=app, model=model )
    except ContentType.DoesNotExist:
        return None
    return obj.model_class()
