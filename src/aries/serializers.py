# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
    SerializerMethodField,
    ReadOnlyField,
)
from rest_framework_recursive.fields import RecursiveField
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from django.contrib.admin.options import get_content_type_for_model
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from collections import OrderedDict

from .models import *

class OwnedMixin( ModelSerializer ):
    owner   = ReadOnlyField( source='owner.user.username' )
    creator = ReadOnlyField( source='creator.user.username' )

    def create( self, validated_data ):
        object = super( OwnedMixin, self ).create( validated_data )
        request = self.context.get( 'request' )
        if request:
            user = request.user
        if not user:
            user = get_user_model().objects.get( username='system' )
        LogEntry.objects.log_action(
            user_id=user.pk,
            content_type_id=get_content_type_for_model( object ).pk,
            object_id=object.pk,
            object_repr=force_text( object ),
            action_flag=ADDITION,
            change_message=[{ 'added': {} }],
        )
        return object

    def update( self, instance, validated_data ):
        object = super( OwnedMixin, self ).update( instance, validated_data )
        request = self.context.get( 'request' )
        if request:
            user = request.user
        if not user:
            user = get_user_model().objects.get( username='system' )
        LogEntry.objects.log_action(
            user_id=user.pk,
            content_type_id=get_content_type_for_model( object ).pk,
            object_id=object.pk,
            object_repr=force_text( object ),
            action_flag=CHANGE,
            change_message=[{ 'changed': { 'fields': validated_data.keys() }}],
        )
        return object

class BaseUserSerializer( ModelSerializer ):
    class Meta:
        model  = User
        fields = (
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
        )


class UserSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model  = User
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
        model  = Group
        fields = (
            'id',
            'name',
            'title',
            'description',
            'active',
            'data',
            'user_set',
            'permissions',
            'policies'
            'roles',
        )
    user_set = UserSerializer( many=True )


class RoleSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model  = Role
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
    users = UserSerializer( many=True )
    groups = GroupSerializer( many=True )


class PolicySerializer( HyperlinkedModelSerializer ):
    class Meta:
        model  = Policy
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
    users  = UserSerializer( many=True )
    groups = GroupSerializer( many=True )
    roles  = RoleSerializer( many=True )


class PermissionSerializer( HyperlinkedModelSerializer ):
    class Meta:
        model  = Permission
        fields = (
            'id',
            'name',
            # 'content_type',
            'codename',
            'title',
            'description',
            'active',
            'data',
            'user_set',
            'group_set',
            'policies',
            'roles',
        )
    user_set  = UserSerializer( many=True )
    group_set = GroupSerializer( many=True )
    policies  = PolicySerializer( many=True )
    roles     = RoleSerializer( many=True )


by_model = dict(
    users       = UserSerializer,
    groups      = GroupSerializer,
    policies    = PolicySerializer,
    permissions = PermissionSerializer,
    roles       = RoleSerializer,
)
