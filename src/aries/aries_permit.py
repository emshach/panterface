from . import permit

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
              ( '#permmissions',
                ( 'add change delete',
                  'user group role permission policy' ))),
            ( 'admin', dict(
                title='Admin Staff',
                is_superuser=True
            )),
          ),
          ( '#roles',
            ( 'manager',
              ( 'user', dict( title='User Manager' ),
                ( '#permissions',
                )),
              ( 'security', dict( title='Security Manager' ),
                ( '#permissions',
                  ( 'add change delete',
                    ( 'user group role policy permission' ),
                    ( 'permissions', 'user group role policy' ),
                    ( 'policy',      'user group role' ),
                    ( 'role',        'user group' ),
                    ( 'group',       'user' ),
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
