# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models as M
from django.contrib.postgres.fields import JSONField
from django.contrib.auth import models as auth
from django_auto_one_to_one import AutoOneToOneModel

Model = M.Model

class _Base( Model ):
    class Meta:
        abstract = True
    title        = M.CharField( blank=True, max_length=255 )
    description  = M.TextField( blank=True )
    active       = M.BooleanField( default=True )


@python_2_unicode_compatible
class Base( _Base ):
    class Meta:
        abstract = True

    def __str__( self ):
        return self.name


class DataMixin( Model ):
    class Meta:
        abstract = True
    data = JSONField( default=dict )


class Permission( AutoOneToOneModel( auth.Permission, related_name='aries_data',
                                     attr='auth_ptr'), Base, DataMixin ):
    pass


class Policy( Base, DataMixin ):
    class Types:
        ALLOW = 'allow'
        DENY = 'deny'
        ALL = (
            ALLOW, 'Allow',
            DENY,  'Deny',
        )
    type = M.CharField( max_length=16, choices=Types.ALL, default=Types.ALLOW )
    permissions = M.ManyToManyField( Permissions, blank=True, related_name='policies' )


class Role( Base, DataMixin ):
    permissions = M.ManyToManyField( Permissions, blank=True, related_name='roles' )
    policies = M.ManyToManyField( Policy, blank=True, related_name='roles' )
    pass


class User( auth.AbstractUser, _Base, DataMixin ):
    anonymous = M.BooleanField( default=False )
    roles = M.ManyToManyField( Role, blank=True, related_name='users' )
    policies = M.ManyToManyField( Policy, blank=True, related_name='users' )


class Group( AutoOneToOneModel( auth.Group, related_name='aries_data',
                                attr='auth_ptr' ), Base, DataMixin ):
    roles = M.ManyToManyField( Role, blank=True, related_name='groups' )
    permissions = M.ManyToManyField( Permissions, blank=True, related_name='groups' )
    policies = M.ManyToManyField( Policy, blank=True, related_name='groups' )


