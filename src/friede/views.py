# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .objects import getregistries, getenv
from .core import setup, setupshell, setuptheme, setupmenus

# Create your views here.
def index( request ):
    env = getenv()
    # # get the shell
    menus = env.C.menus()
    if not menus:
        menus = setupmenus()
    shell = env.H.current()
    if not shell:
        shell = setupshell( env )
    # and the selected theme for that shell
    theme = shell.T.current()
    if not theme:
        theme = setuptheme( shell )
    # TODO: DoesNotExistException
    context = dict(
        shell=shell,
        theme=theme,
        menus=menus,
    )
    for registry in getregistries():
        context[ registry.name ] = registry
    return render( request, theme.home, context )
