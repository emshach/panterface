from . import permit

def _perm_name( name, data={} ):
    return "Can {} {}".format(*( name[:2] ))

def _aries_model( ct, data={} ):
    return 'aries.'+ct

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
            ( 'power', dict( title='Power-users' )),
            ( 'staff', dict(
                title='Internal Staff',
                is_staff=True
            ),
              ( '#permissions',
                ( 'add change delete',
                  'user group role policy permission',
                  dict( ct=_aries_model, name=_perm_name )))),
            ( 'admin', dict(
                title='Admin Staff',
                is_staff=True,
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
                    ( 'user group role policy permission',
                      dict( ct=_aries_model, name=_perm_name )),
                    ( 'permissions',
                      'user group role policy',
                      dict( ct=_aries_model, name=_perm_name_trans_1 )),
                    ( 'policy',
                      'user group role',
                      dict( ct=_aries_model, name=_perm_name_trans_1 )),
                    ( 'role',
                      'user group',
                      dict( ct=_aries_model, name=_perm_name_trans_1 )),
                    ( 'group',
                      'user', dict( ct='users', name=_perm_name_trans_1 )),
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
