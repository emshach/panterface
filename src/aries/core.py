# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from guardian.core import ObjectPermissionChecker
from .models import owned, Permission
from . import permit

def setup_permissions():
    for model in owned:
        name = model._meta.model_name
        verbose = model._meta.verbose_name
        ct = ContentType.objects.get_for_model( model )
        Permission.objects.get_or_create(
            defaults=dict( name="Can change own {}".format( verbose )),
            codename="change_own_{}".format( name ),
            content_type=ct )
        Permission.objects.get_or_create(
            defaults=dict( name="Can delete own {}".format( verbose )),
            codename="delete_own_{}".format( name ),
            content_type=ct )
        Permission.objects.get_or_create(
            defaults=dict( name="Can see {}".format( verbose )),
            codename="see_{}".format( name ),
            content_type=ct )
        Permission.objects.get_or_create(
            defaults=dict( name="Can see own {}".format( verbose )),
            codename="see_own_{}".format( name ),
            content_type=ct )
        Permission.objects.get_or_create(
            defaults=dict( name="Can view {}".format( verbose )),
            codename="view_{}".format( name ),
            content_type=ct )
        Permission.objects.get_or_create(
            defaults=dict( name="Can view own {}".format( verbose )),
            codename="view_own_{}".format( name ),
            content_type=ct )
    permit.setup()

def owned_by( obj, user ):
    if not ( getattr( obj, 'owner', None )):
        return False
    return obj.owner.user is user

def can( perm, user, model, obj, check=None ):
    if not check:
        check = ObjectPermissionChecker( user )
    return check.has_perm( "{}_{}".format( perm, model), obj )\
        or ( owned_by( obj, user )
             and check.has_perm( "{}_own_{}".format( perm, model), obj ))
