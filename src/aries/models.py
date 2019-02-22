# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models as M
from django.contrib.auth.models import AbstractUser



### custom user model

class User( AbstractUser ):
    pass
