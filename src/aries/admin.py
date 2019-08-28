# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register( User, UserAdmin )
admin.site.register( Permission )
admin.site.register( Policy )
admin.site.register( Role )
admin.site.register( User )
admin.site.register( Group )
admin.site.register( Permit )
admin.site.register( Ownership )
admin.site.register( Creation )
