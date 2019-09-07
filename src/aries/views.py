# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Max, Value
from django.shortcuts import render
from django.contrib.auth import authenticate, login as authlogin, logout as authlogout
from django.contrib.admin.models import LogEntry
from rest_framework import status, viewsets, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .auth import get_user
from .models import *
from .serializers import *
import json
import time
import base64
import re

def _get_model( name ):
    app, model = name.split('.')
    try:
        obj = ContentType.objects.get( app_label=app, model=model )
    except ContentType.DoesNotExist:
        return None
    return obj.model_class()

def login( request ):
    pass

def logout( request ):
    pass

def register( request ):
    pass

@api_view([ 'POST' ])
@permission_classes(( permissions.AllowAny, ))
def api_login( request ):
    time.sleep(3)
    user     = request.user
    params   = request.data
    username = params.get( 'username' )
    email    = params.get( 'email' )
    phone    = params.get( 'phone' )
    password = params.get( 'password' )
    try:
        applicant = User.objects.get( username=username ) if username \
            else User.objects.get( email=email ) if email \
                 else User.objects.get( phone=phone ) if phone else None
    except User.DoesNotExist:
        return Response( dict( error='Invalid credentials'), status=401 )
    if not applicant.anonymous:
        applicant = authenticate( request, username=applicant.username,
                                  password=password )

    if not applicant:
        return Response( dict( error='Invalid credentials'), status=401 )
    else:
        authlogin( request, applicant )
        return Response( dict(
            success='logged in!',
            user=UserSerializer( applicant, context=dict( request=request )).data ))

@api_view([ 'GET', 'POST' ])
@permission_classes(( permissions.AllowAny, ))
def api_logout( request ):
    authlogout( request )
    anon = authenticate( request )
    if anon and anon.anonymous:
        authlogin( request, anon )
    return Response( dict(
        success='logged out!',
        user=UserSerializer( anon, context=dict( request=request )).data ))

@api_view([ 'POST' ])
@permission_classes(( permissions.AllowAny, ))
def api_register( request ):
    time.sleep(3)
    user     = request.user
    params   = request.data
    username = params.get( 'username' )
    fname    = params.get( 'fname' )
    lname    = params.get( 'lname' )
    email    = params.get( 'email' )
    phone    = params.get( 'phone' )
    password = params.get( 'password' )
    try:
        found = User.objects.get( username=username, anonymous=False )\
            if username and username != user.username else None
        if found:
            return Response( dict( error="username '{}' is alraedy in use" ))
    except User.DoesNotExist:
        pass
    try:
        found = User.objects.get( email=email ) if email else None
        if found:
            return Response( dict( error="email '{}' is alraedy in use" ))
    except User.DoesNotExist:
        pass
    try:
        found = User.objects.get( phone=phone ) if phone else None
        if found:
            return Response( dict( error="phone number '{}' is alraedy in use" ))
    except User.DoesNotExist:
        pass

    uname = username or re.sub( r'[+/=]', '+',
                                base64.urlsafe_b64encode( str( randint( 0, 10000000 ))))
    applicant = user if user.anonymous \
    else User.objects.create( username=uname, email=email, first_name=fname,
                              last_name=lname, phone=phone )

    if not password:
        password = ' '.join([ re.sub(
            r'[+/=]', '', base64.urlsafe_b64encode(
                str( randint( 0, randint( 1, 10000000 ))))) for x in range(4) ])
    if applicant.anonymous:
        applicant.anonymous = False
    if not username:
        applicant.username = "user%d" % applicant.id
    applicant.set_password( password )
    applicant.save()
    applicant = authenticate( request, username=applicant.username,
                              password=password )
    login( request, applicant )
    return Response( dict(
        success='signed up!',
        user=UserSerializer( applicant, context=dict( request=request )).data ))

@api_view([ 'GET' ])
@permission_classes(( permissions.AllowAny, ))
def api_auth_status( request ):
    pass


@api_view([ 'GET' ])
@permission_classes(( permissions.AllowAny, ))
def api_can( request, perm='any', format=None ):
    user = request.user
    if user.is_superuser:
        return Response( True )
    try:
        op, app, model = perm.split('.')
    except ValueError:
        return Response( None )

    perm = user.has_perm( "{}.{}_{}".format( app, op, model )) and 'global'
    if not perm and user.has_perm( "{}.{}_own_{}".format( app, op, model )):
        perm = 'user'
    return Response( perm )

@api_view([ 'GET' ])
@permission_classes(( permissions.AllowAny, ))
def api_which_can( request, format=None ):
    user = request.user
    perms = set( request.query_params.getlist( 'op' ))
    out = {}
    if user.is_superuser:
        return Response({ x: True for x in perms })
    for p in perms:
        op, app, model = p.split('.')
        out[p] = user.has_perm( "{}.{}_{}".format( app, op, model )) and 'global'
        if not out[p]:
            out[p] = user.has_perm( "{}.{}_own_{}".format( app, op, model )) and 'user'
    return Response( out )

@api_view([ 'GET' ])
@permission_classes(( permissions.AllowAny, ))
def api_userdata( request, sub='', format=None ):
    subs = sub.split('+') if sub else None;
    user = request.user
    owned = user.owned
    if subs:
        subs = filter( lambda x: x, map( _get_model, subs ))
        if subs:
            owned = owned.filter( content_type__in=subs )
    secondary = []
    body = []
    for o in owned.all():
        ct = o.content_type
        mod = "{}.{}".format( ct.app_label, ct.model )
        od = dict( id=o.owned.id, model=mod )
        o = o.owned
        body.append( od )
        for attr in ( 'name', 'path', 'title', 'description' ):
            od[ attr ] = getattr( o, attr, None )
        try:
            logs = LogEntry.objects.filter( content_type=ct.pk, object_id=o.pk )
            od[ 'count' ] = logs.count()
            od[ 'modified' ] = logs.latest( 'action_time' ).action_time.isoformat()
            primary.append( od )
            secondary.append( od )
        except LogEntry.DoesNotExist:
            od[ 'count' ] = 0
            od[ 'modified' ] = 0
    primary = sorted( primary, key=lambda x: x[ 'count' ], reverse=True )[:10]
    secondary = sorted( secondary, key=lambda x: x[ 'modified' ], reverse=True )[:100]
    return Response( dict(
        primary=primary,
        secondary=secondary,
        body=body
    ))

class OwnedViewMixin( viewsets.ModelViewSet ):
    def perform_create( self, serializer ):
        obj = serializer.save()
        owner = Ownership.objects.create( user=self.request.user, owned=obj )


class UserViewSet( viewsets.ModelViewSet ):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet( viewsets.ModelViewSet ):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PolicyViewSet( viewsets.ModelViewSet ):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer


class PermissionViewSet( viewsets.ModelViewSet ):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class RoleViewSet( viewsets.ModelViewSet ):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


