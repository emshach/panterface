# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

def snake_case( str ):
    return re.sub(r'(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', r'_\1', str )\
             .lower().strip('_')

def split_dict( obj, *keys ):
    d1 = {}
    d2 = {}
    for key, value in obj.items():
        ( d1 if key in keys else d2 )[ key ] = value
    return d1, d2

def as_tree( col, field='path', sep='.' ):
    tree = {}
    for item in col:
        node = tree
        path = getattr( item, field ).split( sep )
        while path and not path[-1]:
            path.pop()
        for x in path:
            if not x: continue
            if x not in node:
                node[x] = {}
            node = node[x]
        node['$'] = item
