# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in
from .permit import permits, rules

def apply_rules( sender, request, user ):
    for _if, _then, _else in rules:
        for op, arg in ( _then if _if( user, request ) else _else ):
            f = getattr( user, op )
            f( arg )

class AriesConfig( AppConfig ):
    name = 'aries'
    def ready( self ):
        user_logged_in.connect( apply_rules )
