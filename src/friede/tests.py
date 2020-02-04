# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .action import Action, actions
from .app import setup
import friede.models as M


class ActionsTestCase( TestCase ):
    def setUp( self ):
        setup([])

    def test_can_retrieve_action_object_by_name( self ):
        """Actions objects can be retrieved by name """
        actionobj = actions.get( 'install' )
        self.assertIsNotNone( actionobj )

    def test_can_retrieve_action_store_by_name( self ):
        actionstore = M.Action.objects.get( name='install' )
        self.assertIsNotNone( actionstore )

    def test_can_retrieve_action_object_by_store( self ):
        """Action retrieval from db and memory works as intended"""
        actionobj = actions.get( 'install' )
        actionstore = M.Action.objects.get( name='install' )
        self.assertIsNotNone( actionobj )
        self.assertIsNotNone( actionstore )
        self.assertIs( actionobj, Action.get_for_object( actionstore ))
