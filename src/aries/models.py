# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import six
from django.db import models as M
from django.contrib.postgres.fields import JSONField
from django.contrib.auth import models as auth
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType

Model = M.Model
owned = set()

class _AutoChildBase( M.base.ModelBase ):
    class Meta:
        abstract = True
    def __new__( mcs, name, bases, attrs ):
        model = super( _AutoChildBase, mcs ).__new__( mcs, name, bases, attrs )

        if model._meta.abstract or model._meta.concrete_model is not model:
            return model

        pk = model._meta.pk
        parents = model._meta.parents
        parent = filter( lambda x: x[1] is pk, parents.items())[0][0]

        def on_create_cb( sender, instance, created, *args, **kwargs ):
            if created:
                m = model(**{ pk.name: instance })
                m.save_base( raw=True )
                m.refresh_from_db()

        post_save.connect(on_create_cb, sender=parent, weak=False)
        return model


class AutoChildModel( six.with_metaclass( _AutoChildBase, Model )):
    class Meta:
        abstract = True


class _Base( Model ):
    class Meta:
        abstract = True
    title        = M.CharField( blank=True, max_length=255 )
    description  = M.TextField( blank=True )
    active       = M.BooleanField( default=True )


@six.python_2_unicode_compatible
class Base( _Base ):
    class Meta:
        abstract = True

    name = M.CharField( max_length=255 )

    def __str__( self ):
        return self.name


class DataMixin( Model ):
    class Meta:
        abstract = True
    data = JSONField( default=dict )


class Permission( AutoChildModel, auth.Permission, _Base, DataMixin ):
    auth_ptr  = M.OneToOneField( auth.Permission, M.CASCADE, parent_link=True,
                                 related_name='aries_data' )

class Policy( Base, DataMixin ):
    class Types:
        ALLOW = 'allow'
        DENY  = 'deny'
        ALL   = (
            ( ALLOW, 'Allow' ),
            ( DENY,  'Deny' ),
        )
    class Functions:
        BASIC      = 'basic'
        UNION      = 'union'
        INTERSECT  = 'intersect'
        USERS      = 'users'
        PERMISSION = 'permission'
        CUSTOM     = 'custom'
        ALL = (
            ( BASIC, 'Basic' ),
            ( UNION, 'Union' ),
            ( INTERSECT, 'Intersection' ),
            ( USERS, 'Users/Groups/Roles' ),
            ( PERMISSION, 'Permissions' ),
            ( CUSTOM, 'Custom' ),
        )
    type        = M.CharField( max_length=16, choices=Types.ALL, default=Types.ALLOW )
    function    = M.CharField( max_length=16, choices=Functions.ALL,
                               default=Functions.BASIC )
    permissions = M.ManyToManyField( Permission, blank=True, related_name='policies' )


class Role( Base, DataMixin ):
    permissions = M.ManyToManyField( Permission, blank=True, related_name='roles' )
    policies = M.ManyToManyField( Policy, blank=True, related_name='roles' )


def _normalize( Type, thing, name='name' ):
    if isinstance( things, (QuerySet, Type )):
        return thing
    if isinstance( thing, int ):
        return Type.objects.get( pk=thing )
    if isinstance( thing, basestring ):
        return Type.objects.get(**{ name : thing })

def _normalize_list( Type, things, name='name' ):
    if isinstance( things, QuerySet ):
        return things
    if not things:
        return ()
    if not filter( lambda x: not isinstance( x, int ), things ):
        return Type.objects.filter( pk__in=things )
    if not filter( lambda x: not isinstance( x, basestring ), things ):
        return Type.objects.filter(**{ name + '__in' : things })
    return filter( lambda x: isinstance( x, Type ),
                   tuple( _normalize( Type, thing, name ) for thing in things ))

class User( auth.AbstractUser, _Base, DataMixin ):
    anonymous = M.BooleanField( default=False )
    roles     = M.ManyToManyField( Role, blank=True, related_name='users' )
    policies  = M.ManyToManyField( Policy, blank=True, related_name='users' )

    def addgroup( self, group ):
        x = _normalize( Group, group )
        if x: self.groups.add(x)

    def rmgroup( self, group ):
        x = _normalize( Group, group )
        if x: self.groups.delete(x)

    def addgroups( self, groups ):
        x = _normalize_list( Group, groups )
        if x: self.groups.add( *x )

    def rmgroups( self, groups ):
        x = _normalize_list( Group, groups )
        if x: self.groups.delete( *x )

    def addrole( self, role ):
        x = _normalize( Role, role )
        if x: self.roles.add(x)

    def rmrole( self, role ):
        x = _normalize( Role, role )
        if x: self.roles.delete(x)

    def addroles( self, roles ):
        x = _normalize_list( Role, roles )
        if x: self.roles.add( *x )

    def rmroles( self, roles ):
        x = _normalize_list( Role, roles )
        if x: self.roles.delete( *x )

    def addpermission( self, perm ):
        x = _normalize( Permission, perm, 'codename' )
        if x: self.user_permissions.add(x)

    def rmpermission( self, perm ):
        x = _normalize( Permission, perm, 'codename' )
        if x: self.user_permissions.delete(x)

    def addpermissions( self, perms ):
        x = _normalize_list( Permission, perms, 'codename' )
        if x: self.user_permissions.add( *x )

    def rmpermissions( self, perms ):
        x = _normalize_list( Permission, perms, 'codename' )
        if x: self.user_permissions.delete( *x )

    def addpolicy( self, policy ):
        x = _normalize( Policy, policy )
        if x: self.policys.add(x)

    def rmpolicy( self, policy ):
        x = _normalize( Policy, policy )
        if x: self.policys.delete(x)

    def addpolicies( self, policies ):
        x = _normalize_list( Policy, policies )
        if x: self.policies.add( *x )

    def rmpolicies( self, policies ):
        x = _normalize_list( Policy, policies )
        if x: self.policies.delete( *x )


class Group( AutoChildModel, auth.Group, _Base, DataMixin ):
    auth_ptr     = M.OneToOneField( auth.Group, M.CASCADE, parent_link=True,
                                 related_name='aries_data' )
    is_superuser = M.BooleanField( default=False )
    is_staff     = M.BooleanField( default=False )
    title        = M.CharField( blank=True, max_length=255 )
    roles        = M.ManyToManyField( Role, blank=True, related_name='groups' )
    policies     = M.ManyToManyField( Policy, blank=True, related_name='groups' )


class Permit( Base ):
    version   = M.CharField( max_length=32, default='0.0.0' )
    available = M.CharField( max_length=32, default='0.0.0' )

class _AutoOwnedBase( M.base.ModelBase ):
    class Meta:
        abstract = True
    def __new__( mcs, name, bases, attrs ):
        model = super( _AutoOwnedBase, mcs ).__new__( mcs, name, bases, attrs )

        if model._meta.abstract or model._meta.concrete_model is not model:
            return model
        owned.add( model )
        return model


class AutoOwnedModel( six.with_metaclass( _AutoOwnedBase, Model )):
    class Meta:
        abstract = True
    owner    = M.ForeignKey( User, related_name="%(app_label)s_%(class)s_set",
                             on_delete=M.CASCADE, blank=True, null=True )
    creator  = M.ForeignKey( User, related_name="%(app_label)s_%(class)s_created_set",
                             on_delete=M.CASCADE, blank=True, null=True )


