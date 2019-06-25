# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import status, viewsets, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
from .serializers import *

def login( request ):
    pass

def logout( request ):
    pass

def register( request ):
    pass

@api_view([ 'GET' ])
@permission_classes(( permissions.AllowAny, ))
def api_can( request, perm='any', format=None ):
    if request.user.is_superuser:
        return Response( True )
    try:
        op, app, model = perm.split('.')
    except ValueError:
        return Response( None )
    return Response( request.user.has_perm( "{}.{}_{}".format( app, op, model )))

@api_view([ 'GET' ])
@permission_classes(( permissions.AllowAny, ))
def api_which_can( request, format=None ):
    user = request.user
    perms = set( request.query_params.getlist( 'op' ))
    out = {}
    if request.user.is_superuser:
        return Response({ x: True for x in perms })
    for p in perms:
        op, app, model = p.split('.')
        out[p] = user.has_perm( "{}.{}_{}".format( app, op, model ))
    return Response( out )

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


