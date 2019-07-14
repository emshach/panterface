from aries import permit

def _friede_model( ct, data={} ):
    return 'friede.' + ct[-1]

def _perm_name( name, data={} ):
    return "Can " + ' '.join( name )

class Permit( permit.Permit ):
    name = 'friede'
    data = (
    ( '0.0.1',
      ( '#groups', 'anonymous authenticated confirmed verified',
        ( '#permissions',
          ( 'install uninstall update activate deactivate', 'own', 'app',
            dict( ct='friede.app', name=_perm_name )))),
      ( '#roles',
        ( 'manager',
          ( 'app', dict( title='App Manager' ),
            ( '#permissions',
              ( 'install uninstall update activate deactivate', 'app',
                dict( ct='friede.app', name=_perm_name )))),
          ( 'site', dict( title='Site Manager' ),
            ( '#permissions',
              ( 'add change delete',
                'widget block screen shell theme location link setting icon action',
                dict( ct=_friede_model, name=_perm_name )))))),
      ( '#groups', 'power staff',
        ( '#roles', ( 'manager', 'app site' ))),
    ),
    )
