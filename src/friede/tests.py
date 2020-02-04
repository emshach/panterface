# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .actions import Action, actions
from .app import setup
import friede.models as M


class ActionsTestCase( TestCase ):
    def setUp( self ):
        setup([])

    def test_can_get_action_object( self ):
        actionobj = actions.get( 'install' )
        actionstore = M.Action.objects.get( name='install' )
        self.assertIsNotNone( actionobj )
        self.assertIsNotNone( actionstore )
        self.assertIs( actionobj, Action.get_for_object( actionstore ))
