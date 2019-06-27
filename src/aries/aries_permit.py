from . import permit

def _perm_name( name, data={} ):
    return "Can {} {}".format(*( name[:2] ))

def _perm_name_trans_1( name, data={} ):
    op, arg1, arg2 = name
    return "Can {} {} {}".format( op, arg2, arg1 )

class Permit( permit.Permit ):
    name = 'aries'
    rules = (( lambda u: u.anonymous,
               (( 'addgroup', 'anonymous' )),
               (( 'rmgroup',  'anonymous' ),
                ( 'addgroup', 'authenticated' ))),)
    data = (
        ( '0.0.1',
          ( '#groups',
            ( 'anonymous', dict( title='Anonymous Users' )),
            ( 'authenticated', dict( title='Authenticated Users' )),
            ( 'confirmed', dict( title='Confirmed Users' )),
            ( 'verified', dict( title='Verified Users' )),
            ( 'power', dict( title='Power-Users' )),
            ( 'staff', dict(
                title='Internal Staff',
                is_staff=True
            ),
              ( '#permissions',
                ( 'add change delete',
                  ( 'user', dict( ct='users', name=_perm_name )),
                  ( 'group', dict( ct='groups', name=_perm_name )),
                  ( 'role', dict( ct='roles', name=_perm_name )),
                  ( 'policy', dict( ct='policies', name=_perm_name )),
                  ( 'permission', dict( ct='permissions', name=_perm_name )),
                ))),
            ( 'admin', dict(
                title='Admin Staff',
                is_superuser=True
            )),
          ),
          ( '#roles',
            ( 'manager',
              ( 'user', dict( title='User Manager' ),
                ( '#permissions',
                  ( 'add change delete',
                    ( 'group role',
                      ( 'user', dict( ct='users', name=_perm_name_trans_1 ))),
                  ))),
              ( 'security', dict( title='Security Manager' ),
                ( '#permissions',
                  ( 'add change delete',
                    ( 'user', dict( ct='users', name=_perm_name_trans_1 )),
                    ( 'group', dict( ct='groups', name=_perm_name_trans_1 )),
                    ( 'role', dict( ct='roles', name=_perm_name_trans_1 )),
                    ( 'policy', dict( ct='policies', name=_perm_name_trans_1 )),
                    ( 'permission', dict( ct='permissions', name=_perm_name_trans_1 )),
                    ( 'permissions',
                      ( 'user', dict( ct='users', name=_perm_name_trans_1 )),
                      ( 'group', dict( ct='groups', name=_perm_name_trans_1 )),
                      ( 'role', dict( ct='roles', name=_perm_name_trans_1 )),
                      ( 'policy', dict( ct='policies', name=_perm_name_trans_1 )),
                    ),
                    ( 'policy',
                      ( 'user', dict( ct='users', name=_perm_name_trans_1 )),
                      ( 'group', dict( ct='groups', name=_perm_name_trans_1 )),
                      ( 'role', dict( ct='roles', name=_perm_name_trans_1 )),
                    ),
                    ( 'role',
                      ( 'user', dict( ct='users', name=_perm_name_trans_1 )),
                      ( 'group', dict( ct='groups', name=_perm_name_trans_1 )),
                    ),
                    ( 'group',
                      ( 'user', dict( ct='users', name=_perm_name_trans_1 )),
                    ),
                  ))),
            )),
          ( '#permissions', ),
          ( '#policies', ),
          ( '#users',
            ( 'system', dict(
                title="System User",
                is_superuser=True,
                is_staff=True
            ))),
        ),
    )
