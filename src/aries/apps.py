# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from .models import owned


class AriesConfig(AppConfig):
    name = 'aries'

    def ready( self ):
        super( AriesConfig, self ).ready()
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
