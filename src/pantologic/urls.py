"""pantologic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import get_user_model

# init aries permissions FIXME: feels hackish
from aries.models import owned, Permission
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

urlpatterns = [
    url( r'^api-auth/', include( 'rest_framework.urls', namespace='rest_framework' )),
    # url( r'^accounts/', include( 'allauth.urls' )),
    url( r'^admin/',    admin.site.urls ),
    url( r'',        include( 'friede.urls', namespace='friede' )),
]
