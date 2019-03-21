# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .objects import Settings, Shells, getenv, getregistries, getshell
from .models import Setting, Shell, Theme, ShellEntry, ThemeEntry

def setup():
    "make new settings"
    # settings = Settings()
    # shell_setting = settings.sys.ui.shell.get_or_create(
    #     type=Setting.Types.Choice,
    #     data=dict(
    #         model='Shell',
    #         registry__parent__name=''
    #     ))
    # maybe not yet
    env = getenv()
    shell = env.H.current
    if not shell:
        shell = Shells().mayflower.get()
        if not shell:
            shell = setupshell( env )

def setupshell( env=None ):
    "make (and select) the default shell"
    if not env:
        env = getenv()
    shell = Shell.objects.create(
        name='shells.mayflower',
        templates='friede/mayflower'
    )
    env.addshell( 'current', shell )
    setuptheme( shell )

def setuptheme( shell=None ):
    "make (and select) the default theme for the current shell"
    if not shell:
        shell = Shells().mayflower.get()
    theme = Theme.objects.create(
        name='themes.acamar',
        templates='friede/mayflower/acamar'
    )
    shell.addtheme( 'current', theme )
