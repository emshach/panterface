# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from importlib import import_module
from packaging.version import parse as version_parse
from django.conf import settings
from collections import OrderedDict, deque
from django.db import transaction
from . import models as M
import traceback
import sys

rules = []
permits = OrderedDict()

def setup():
    from . import aries_permit
    try:
        permits[ 'aries' ] = aries_permit.Permit()
        for app_name in settings.INSTALLED_APPS:
            if app_name == 'aries': continue
            name = app_name
            module = app_name
            if module:
                try:
                    permit = import_module( "%s.aries_permit" % module )
                    permits[ module ] = permit.Permit()
                except ( ImportError, AttributeError ) as e:
                    msg = str(e)
                    if 'No module named aries_permit' not in msg:
                        print >> sys.stderr, 'got exception', type(e), e,\
                            "in friede.urls/%s" % module
                        traceback.print_exc()
                    continue        # TODO: maybe warn
    except Exception:
        # pass                        # TODO: handle
        raise

class Permit( object ):
    rules = ()
    data = ()
    model = None
    name = ''
    def __init__( self ):
        super( Permit, self ).__init__()
        self.model, _ = M.Permit.objects.get_or_create( name=self.name )
        self.installrules()
        self.installdata()

    def installrules( self ):
        rules.extend([ (r,) + ((),) if len(r) < 3 else r[:3] for r in self.rules ])

    def installdata( self ):
        version = self.version
        available = None
        error = None
        types = dict(
            users=M.User,
            groups=M.Group,
            roles=M.Role,
            permissions=M.Permission,
            policies=M.Policy,
        )
        names = dict(
            users=lambda x: '_'.join(x),
            groups=lambda x: '.'.join(x),
            roles=lambda x: '.'.join(x),
            permissions=lambda x: '_'.join(x),
            policies=lambda x: '.'.join(x),
        )
        namefields = dict(
            users='username',
            groups='name',
            roles='name',
            permissions='codename',
            policies='name',
        )
        def set_superuser( user ):
            user.is_superuser=True
            user.save()
        ops = dict(
            superuser=set_superuser
        )
        def update_version ():
            self.version = available

        for tree in self.data:
            v = version_parse( tree[0] )
            print 'installing permit', v
            available = v
            if error or v <= version:
                continue
            with transaction.atomic():
                transaction.on_commit( update_version )
                stack = deque([ tree[1:] ])
                name = deque([''])
                data = deque()
                model = deque()
                cr = deque([()])

                def mkobject( Type, name=None, data={}):
                    if data.get( 'name' ):
                        if callable( data[ 'name' ]):
                            name = data['name']( name )
                        else:
                            name = data.pop( 'name' )
                    reg = registry[0]
                    if isinstance( name, ( tuple, list )):
                        name = names[ reg ]( name )
                    obj, new = Type.objects.update_or_create(
                        defaults=data,
                        **{ namefields[ reg ]: name })
                    print 'created' if new else 'updated', Type._meta.model_name,\
                        name
                    return obj

                def mkobjects( attrs={} ):
                    if cr[0] or not model[0] or not data[0]:
                        return
                    cr[0] = tuple( map(
                        lambda x: mkobject( types[ model[0] ], x, attrs ),
                        data[0] ))

                def popstack():
                    stack.pop()

                def poppath():
                    path.popleft()

                def popmodel():
                    model.popleft()

                def popcr():
                    objects = cr.popleft()
                    parents = cr[0]
                    if not parents: return
                    tag = model[0]
                    rel = 'user_permissions' \
                        if tag == 'permissions' and model[1] == 'users' \
                        else tag
                    for p in parents:
                        getattr( p, rel ).add( *objects )
                        print 'added', objects, 'to', p

                def poperate():
                    mkobject()
                    path.popleft()
                    data.popleft()

                def popdata():
                    data.popleft()
                try:
                    while stack:
                        top = stack.pop()
                        if isinstance( top, tuple ):
                            if not len( top ):
                                continue
                            tag = top[0]
                            body = top[1:]
                            if isinstance( tag, basestring ):
                                if tag.startswith('#'):
                                    tag = tag[1:]
                                    mkobjects()
                                    if tag in ops:
                                        if cr[0]:
                                            ops[tag]( cr[0] )
                                    elif tag in types:
                                        model.appendleft( tag )
                                        cr.appendleft( None )
                                        data.appendleft()
                                        stack.extend(( popdata, popmodel, popcr ))
                                        stack.extend( body[::-1] )

                                else:
                                    tag = map( lambda x: (x,),
                                               filter( lambda x: x, tag.split()))
                            if isinstance( tag, list ):
                                items = tuple(
                                    x + y for x in data[0] for y in tag
                                ) if len( data ) else tag
                                data.appendleft( items )
                                stack.append( popdata if len( body ) else poperate )
                        elif isinstance( top, list ):
                            stack.extend( tuple(( x, {} ) for x in top[ ::-1 ]))
                        elif isinstance( top, dict ):
                            mkobjects( top )
                        elif isinstance( top, basestring ):
                            stack.append(( top, ))
                        elif callable( top ):
                            top()
                except Exception as e:
                    print >> sys.stderr, "got exception", type(e), e
                    traceback.print_exc()
                    error = True
                    break

        self.available = available

    @property
    def version( self ):
        return version_parse( self.model.version )

    @version.setter
    def version( self, version ):
        self.model.version = str( version )
        self.model.save()

    @property
    def available( self ):
        return version_parse( self.model.available )

    @available.setter
    def available( self, available ):
        self.model.available = str( available )
        self.model.save()

