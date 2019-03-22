# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

def snake_case( str ):
    return re.sub(r'(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', r'_\1', str )\
             .lower().strip('_')

