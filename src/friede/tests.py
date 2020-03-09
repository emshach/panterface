# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import get_user_model
from .action import Action, actions, Operation
from .app import apps
from .util import toversion
from . import models as M
from . import views as V
from . import urls
import pprint

success, _ = M.ActionStatus.objects.get_or_create(
    name='success',
    defaults=dict( goodness=1.0 )
)
failed, _ = M.ActionStatus.objects.get_or_create(
    name='failed',
    defaults=dict( goodness=-1.0 )
)
M.ActionStatus.objects.get_or_create(
    name='init',
    defaults=dict( goodness=0.0 )
)
M.ActionStatus.objects.get_or_create(
    name='parent_aborted',
    defaults=dict( goodness=-0.5 )
)
M.ActionStatus.objects.get_or_create(
    name='invalid_operation',
    defaults=dict( goodness=-10.0 )
)
M.ActionStatus.objects.get_or_create(
    name='app_installed',
    defaults=dict( parent=success )
)
M.ActionStatus.objects.get_or_create(
    name='app_install_failed',
    defaults=dict( parent=failed )
)
M.ActionStatus.objects.get_or_create(
    name='app_reinstalled',
    defaults=dict( parent=success )
)
M.ActionStatus.objects.get_or_create(
    name='app_reinstall_failed',
    defaults=dict( parent=failed )
)
M.ActionStatus.objects.get_or_create(
    name='app_uninstalled',
    defaults=dict( parent=success )
)
M.ActionStatus.objects.get_or_create(
    name='app_uninstall_failed',
    defaults=dict( parent=failed )
)
M.ActionStatus.objects.get_or_create(
    name='app_updated',
    defaults=dict( parent=success )
)
M.ActionStatus.objects.get_or_create(
    name='app_update_failed',
    defaults=dict( parent=failed )
)
M.ActionStatus.objects.get_or_create(
    name='app_activated',
    defaults=dict( parent=success )
)
M.ActionStatus.objects.get_or_create(
    name='app_activation_failed',
    defaults=dict( parent=failed )
)
M.ActionStatus.objects.get_or_create(
    name='app_deactivated',
    defaults=dict( parent=success )
)
M.ActionStatus.objects.get_or_create(
    name='app_deactivation_failed',
    defaults=dict( parent=failed )
)
M.ActionStatus.objects.get_or_create(
    name='app_installed_for_user',
    defaults=dict( parent=success )
)
M.ActionStatus.objects.get_or_create(
    name='app_install_for_user_failed',
    defaults=dict( parent=failed )
)
M.ActionStatus.objects.get_or_create(
    name='app_uninstalled_for_user',
    defaults=dict( parent=success )
)
M.ActionStatus.objects.get_or_create(
    name='app_uninstall_for_user_failed',
    defaults=dict( parent=failed )
)
M.ActionStatus.objects.get_or_create(
    name='app_activated_for_user',
    defaults=dict( parent=success )
)
M.ActionStatus.objects.get_or_create(
    name='app_activate_for_user_failed',
    defaults=dict( parent=failed )
)
M.ActionStatus.objects.get_or_create(
    name='app_deactivated_for_user',
    defaults=dict( parent=success )
)
M.ActionStatus.objects.get_or_create(
    name='app_deactivate_for_user_failed',
    defaults=dict( parent=failed )
)


class ActionsTestCase( TestCase ):
    def test_000_action_by_name( self ):
        "Can retrieve action object by name"
        actionobj = actions.get( 'install' )
        self.assertIsNotNone( actionobj, "Install action exists" )

    def test_001_store_by_name( self ):
        "Can retrieve action store by name"
        actionstore = M.Action.objects.get( name='install' )
        self.assertIsNotNone( actionstore, "Install action object exists" )

    def test_002_action_by_store( self ):
        "Can retrieve action object by store"
        actionobj = actions.get( 'install' )
        actionstore = M.Action.objects.get( name='install' )
        self.assertIsNotNone( actionobj, "Install action exists" )
        self.assertIsNotNone( actionstore, "Install action object exists" )
        self.assertIs( actionobj, Action.get_for_object( actionstore ),
                       "Action object retrieved directly is same as action "
                       "object retrieved by store" )


class AppsTestCase( TestCase ):
    def test_000_core_apps_installed( self ):
        "All core apps automatically installed"
        required = M.App.objects.filter( required=True )
        notinstalled = required.filter( installed=False )
        print 'required apps', required.all()
        self.assertGreater( required.count(), 0,
                            "Required applications exist" )
        self.assertFalse( notinstalled.count(),
                          "All required applications are installed" )

    def test_001_app_by_name( self ):
        "Can get app by name"
        friede = apps.get( 'friede' )
        self.assertIsNotNone( friede, "Got main app from apps registry" )

    def test_002_app_versions( self ):
        "Can get app versions"
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
        cls.mkrequests = RequestFactory()
        cls.client = Client()
        cls.client.force_login( cls.uer )

    def test_000_create_op_object( self ):
        "Can create operation object"
        op = Operation(
            self.user,
            action='install',
            model='friede.app',
            id=4,
            kw={ 'version': '0.2.9' }
        )
        print 'op'
        print dict( op.__dict__, **op.store.__dict__ )
        self.assertIsInstance( op, Operation, "Operation object created" )

    def test_001_op_by_store( self ):
        "Can retrieve operation object by store"
        from datadiff import diff
        op = Operation(
            self.user,
            action='install',
            model='friede.app',
            id=4,
            kw={ 'version': '0.2.9' }
        )
        op2 = Operation( self.user, store=op.store )
        print 'op2'
        print dict( op2.__dict__, **op2.store.__dict__ )
        print diff( op.__dict__, op2.__dict__ )
        self.assertDictEqual(
            op.__dict__, op2.__dict__,
            "Operation retrieved by store is same as original" )

    def test_002_actions_processed( self ):
        "Actions processed with endorsements, permissions, and dependencies"
        res = self.client.post( '/api/do/install/friede.app/335',
                                dict( version='0.1.0' ))
        print 'response'
        pprint.pprint( res.__dict__ )
