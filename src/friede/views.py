# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .objects import Shells, Settings, getregistries, getshell
from .core import setup, setupshell, setuptheme

# Create your views here.
def index( request ):
    settings = Settings()
    # shell_setting = settings.sys.ui.shell()
    # if not shell_setting:
    #     setup()
    #     shell_setting = settings.sys.ui.shell()
    # # get the shell
    shell = Shells().active()
    if not shell:
        shell = setupshell()
    # and the selected theme for that shell
    theme = shell.T.current()
    if not theme:
        theme = setuptheme()
    # TODO: DoesNotExistException
    context = dict(
        shell=shell,
        theme=theme,
    )
    for registry in getregistries():
        context[ registry.name ] = registry
    return render( request, theme.home, context )
