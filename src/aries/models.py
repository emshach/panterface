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

    def __str__( self ):
        return self.name


class DataMixin( Model ):
    class Meta:
        abstract = True
    data = JSONField( default=dict )


class Permission( AutoChildModel, auth.Permission, Base, DataMixin ):
    auth_ptr  = M.OneToOneField( auth.Permission, M.CASCADE, parent_link=True,
                                 related_name='aries_data' )

class Policy( Base, DataMixin ):
    class Types:
        ALLOW = 'allow'
        DENY = 'deny'
        ALL = (
            ( ALLOW, 'Allow' ),
            ( DENY,  'Deny' ),
        )
    type        = M.CharField( max_length=16, choices=Types.ALL, default=Types.ALLOW )
    permissions = M.ManyToManyField( Permission, blank=True, related_name='policies' )


class Role( Base, DataMixin ):
    permissions = M.ManyToManyField( Permission, blank=True, related_name='roles' )
    policies = M.ManyToManyField( Policy, blank=True, related_name='roles' )


class User( auth.AbstractUser, _Base, DataMixin ):
    anonymous = M.BooleanField( default=False )
    roles     = M.ManyToManyField( Role, blank=True, related_name='users' )
    policies  = M.ManyToManyField( Policy, blank=True, related_name='users' )


class Group( AutoChildModel, auth.Group, Base, DataMixin ):
    auth_ptr  = M.OneToOneField( auth.Group, M.CASCADE, parent_link=True,
                                 related_name='aries_data' )
    title     = M.CharField( blank=True, max_length=255 )
    roles     = M.ManyToManyField( Role, blank=True, related_name='groups' )
    policies  = M.ManyToManyField( Policy, blank=True, related_name='groups' )


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


