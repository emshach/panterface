# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth import get_user_model
from .action import Action, actions, Operation
from .app import apps
from .util import toversion
from . import models as M
from . import urls


class ActionsTestCase( TestCase ):
    def test_Can_retrieve_action_object_by_name( self ):
        actionobj = actions.get( 'install' )
        self.assertIsNotNone( actionobj, "Install action exists" )

    def test_Can_retrieve_action_store_by_name( self ):
        actionstore = M.Action.objects.get( name='install' )
        self.assertIsNotNone( actionstore, "Install action object exists" )

    def test_Can_retrieve_action_object_by_store( self ):
        actionobj = actions.get( 'install' )
        actionstore = M.Action.objects.get( name='install' )
        self.assertIsNotNone( actionobj, "Install action exists" )
        self.assertIsNotNone( actionstore, "Install action object exists" )
        self.assertIs( actionobj, Action.get_for_object( actionstore ),
                       "Action object retrieved directly is same as action "
                       "object retrieved by store" )


class AppsTestCase( TestCase ):
    def test_All_core_apps_automatically_installed( self ):
        required = M.App.objects.filter( required=True )
        notinstalled = required.filter( installed=False )
        print 'required apps', required.all()
        self.assertGreater( required.count(), 0,
                            "Required applications exist" )
        self.assertFalse( notinstalled.count(),
                          "All required applications are installed" )

    def test_Can_get_app_by_name( self ):
        friede = apps.get( 'friede' )
        self.assertIsNotNone( friede, "Got main app from apps registry" )

    def test_Can_get_app_versions( self ):
        friede = apps.get( 'friede' )
        print 'friede versions'
        print friede.versions
        self.assertListEqual(
            friede.getversions( '0.2.9', op='<' ),
            [
                toversion( '0.1.0' ),
                toversion( '0.2.0' ),
                toversion( '0.2.1' ),
                toversion( '0.2.3' ),
                toversion( '0.2.4' ),
                toversion( '0.2.5' ),
                toversion( '0.2.6' ),
                toversion( '0.2.7' ),
                toversion( '0.2.8' ),
            ],
            "App versions retrieved properly" )


class OpsTestCase( TestCase ):
    @classmethod
    def setUpTestData( cls ):
        cls.user = get_user_model().objects.get( username='system' )

    def test_Can_create_operation_object( self ):
        op = Operation(
            self.user,
            action='install',
            model='friede.app',
            id=4,
            kw={ 'version': '0.2.9' }
        )
        print 'op'
        print op.__dict__
