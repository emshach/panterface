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

class UserSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = User
        fields = (
            'url',
            'id',
            'last_login',
            'is_superuser',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'date_joined',
            'title',
            'description',
            'active',
            'data',
            'anonymous',
            'groups',
            'user_permissions',
            'policies',
            'roles',
        )


class GroupSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'title',
            'description',
            'active',
            'data',
            'user',
            'permissions',
            'policies'
            'roles',
        )
    user = UserSerializer( many=True )


class RoleSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Role
        fields = (
            'id',
            'title',
            'description',
            'active',
            'data',
            'users',
            'groups',
            'permissions',
            'policies'
        )
    user = UserSerializer( many=True )
    group = GroupSerializer( many=True )


class PolicySerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Policy
        fields = (
            'id',
            'title',
            'description',
            'active',
            'data',
            'type',
            'users',
            'groups',
            'permissions'
            'roles',
        )
    user = UserSerializer( many=True )
    group = GroupSerializer( many=True )
    role = RoleSerializer( many=True )


class PermissionSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model = Permission
        fields = (
            'id',
            'name',
            'content_type',
            'codename',
            'title',
            'description',
            'active',
            'data',
            'user',
            'group',
            'policies',
            'roles',
        )
    user = UserSerializer( many=True )
    group = GroupSerializer( many=True )
    policy = PolicySerializer( many=True )
    role = RoleSerializer( many=True )


by_model = dict(
    users       = UserSerializer,
    groups      = GroupSerializer,
    policies    = PolicySerializer,
    permissions = PermissionSerializer,
    roles       = RoleSerializer,
)
