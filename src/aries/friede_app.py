from __future__ import unicode_literals
from friede import app
from . import views, serializers

class App( app.App ):
    name        = 'aries'
    actions     = 'list view new edit report delete'.split()
    icon        = 'fontawesome.user-tie'
    module      = 'aries'
    title       = 'Project Aries'
    description = '''System-wide User and user relationship functionality including
    groups, roles, security and maintaining a single identity across apps and platforms'''

    objects = '''user group policy permission role permit userconnectiontype
                  userconnection invite view share post'''.split()

    min_version = '0.0.1'
    required = True
    user_required = True

    relations = dict(
        user={
            'model'  : 'User',
            'icon'   : 'fontawesome.user',
            'plural' : 'users',
            'has'    : (),
            'in'     : (),
            'links'  : (),
        },
        group={
            'model'  : 'Group',
            'icon'   : 'fontawesome.users',
            'plural' : 'groups',
            'has'    : (),
            'in'     : (),
            'links'  : (),
        },
        policy={
            'model'  : 'Policy',
            'icon'   : 'fontawesome.file-signature',
            'plural' : 'policies',
            'has'    : (),
            'in'     : (),
            'links'  : (),
        },
        permission={
            'model'  : 'Permission',
            'icon'   : 'fontawesome.key',
            'plural' : 'permissions',
            'has'    : (),
            'in'     : (),
            'links'  : (),
        },
        role={
            'model'  : 'Role',
            'icon'   : 'fontawesome.user-md',
            'plural' : 'roles',
            'has'    : (),
            'in'     : (),
            'links'  : (),
        },
        permit={
            'model'  : 'Permit',
            'icon'   : 'fontawesome.user-md',
            'plural' : 'permits',
            'has'    : (),
            'in'     : (),
            'links'  : (),
        },
        userconnectiontype={
            'model'  : 'UserConnectionType',
            'icon'   : 'fontawesome.user-md',
            'plural' : 'user connection types',
            'has'    : (),
            'in'     : (),
            'links'  : (),
        },
        userconnection={
            'model'  : 'userConnection',
            'icon'   : 'fontawesome.user-md',
            'plural' : 'user connections',
            'has'    : (),
            'in'     : (),
            'links'  : (),
        },
        invite={
            'model'  : 'Invite',
            'icon'   : 'fontawesome.user-md',
            'plural' : 'invites',
            'has'    : (),
            'in'     : (),
            'links'  : (),
        },
        view={
            'model'  : 'View',
            'icon'   : 'fontawesome.user-md',
            'plural' : 'views',
            'has'    : (),
            'in'     : (),
            'links'  : (),
        },
        share={
            'model'  : 'Share',
            'icon'   : 'fontawesome.user-md',
            'plural' : 'shares',
            'has'    : (),
            'in'     : (),
            'links'  : (),
        },
        post={
            'model'  : 'Post',
            'icon'   : 'fontawesome.user-md',
            'plural' : 'posts',
            'has'    : (),
            'in'     : (),
            'links'  : (),
        },
    )
    api=(
        ( r'can/(?P<perm>.+$)',     ( views.api_can,         'can',        [ 'any' ] )),
        ( r'can/?$',                ( views.api_which_can,   'which_can'             )),
        ( r'login/?$',              ( views.api_login,       'login'                 )),
        ( r'logout/?$',             ( views.api_logout,      'logout'                )),
        ( r'register/?$',           ( views.api_register,    'register'              )),
        ( r'auth-status/?$',        ( views.api_auth_status, 'auth-status'           )),
        ( r'userdata/?(?P<sub>.*$)', ( views.api_userdata,   'userdata',   [ '' ]    )),
        ( r'userconnections/?$',
          ( views.api_userconnections, 'userconnections', [ '' ] )),
        ( r'share/?$',              ( views.api_share,       'share',                )),
    )
    routes=(
        ( 'users',               views.UserViewSet               ),
        ( 'groups',              views.GroupViewSet              ),
        ( 'policies',            views.PolicyViewSet             ),
        ( 'permissions',         views.PermissionViewSet         ),
        ( 'roles',               views.RoleViewSet               ),
        ( 'permits',             views.PermitViewSet             ),
        ( 'userconnectiontypes', views.UserConnectionTypeViewSet ),
        ( 'userconnections',     views.UserConnectionViewSet     ),
        ( 'invites',             views.InviteViewSet             ),
        ( 'views',               views.ViewViewSet               ),
        ( 'shares',              views.ShareViewSet              ),
        ( 'posts',               views.PostViewSet               ),
    )
    serializers=(
        ( 'users',               serializers.UserSerializer               ),
        ( 'groups',              serializers.GroupSerializer              ),
        ( 'policies',            serializers.PolicySerializer             ),
        ( 'permissions',         serializers.PermissionSerializer         ),
        ( 'roles',               serializers.RoleSerializer               ),
        ( 'permits',             serializers.PermitSerializer             ),
        ( 'userconnectiontypes', serializers.UserConnectionTypeSerializer ),
        ( 'userconnections',     serializers.UserConnectionSerializer     ),
        ( 'invites',             serializers.InviteSerializer             ),
        ( 'views',               serializers.ViewSerializer               ),
        ( 'shares',              serializers.ShareSerializer              ),
        ( 'posts',               serializers.PostSerializer               ),
    )
    @property
    def data( self ):
        return (
        ( '0.0.2',
          ( '#actions',
            ( 'grant', dict(
                icon='fontawesome.user-check',
                title='Grant permission(s) to a user',
                description='''Attach permissions to a user, giving them access''',
                data=dict(
                    reverse='revoke',
                    component='Gatekeeper',
            ))),
            ( 'revoke', dict(
                icon='fontawesome.user-times',
                title='Revoke a user\'s permission(s)',
                description='''Detach permissions from a user, revoking access''',
                data=dict(
                    reverse='grant',
                    component='Gatekeeper',
            ))),
          )),
        ( '0.0.3',
          dict(
              depends={ 'friede': '0.2.10' }
          ),
          ( '#blocks',
            ( 'viewer',
              ( 'objects', dict(
                  data=dict(
                      component='ObjectViewer'
                  ))))),
          ( '#screens',
            ( 'dashboard',
              ( 'user', dict(
                  icon='fontawesome.user',
                  extends='dashboard',
                  data=dict(
                      component='UserDashboard',
                  )),
                ( 'home', dict(
                    icon='fontawesome.bed',
                    extends='dashboard.user',
                    data=dict(
                        component='UserHomeDashboard',
                    ))),
                ( 'objects', dict(
                    icon='fontawesome.cube',
                    extends='dashboard.sectional' ),
                  ( '#blocks',
                    ( 'primary',
                      dict(
                          path='viewer.objects',
                          entry=dict(
                              data=dict(
                                  mode='featured'
                              )))),
                    ( 'secondary',
                      dict(
                          path='viewer.objects',
                          entry=dict(
                              data=dict(
                                  mode='recent'
                              )))),
                    ( 'body', dict( path='viewer.objects' ))))
              )),
            ( 'page.user', dict(
                icon='fontawesome.home',
                data=dict(
                    component='UserPage',
                )),
              ( 'home', dict(
                  icon='fontawesome.home',
                  data=dict(
                      component='UserHomePage',
                  ))),
              ( 'profile', dict(
                  icon='fontawesome.home',
                  data=dict(
                      component='UserProfilePage',
                  ))),
              ( 'objects', dict(
                  icon='fontawesome.cube',
                  data=dict(
                      component='UserObjectsPage'
                  ))),
            )
          ),
          ( '#locations',
            ( 'from relations', self.objects, self.relations ),
            ( 'user',
              ( 'private', dict(
                  title='My Page',
                  href='/me' ),
                ( '#screens',
                  ( 'default', dict( path='dashboard.user.home' ))),
                ( 'profile', dict(
                    title='My Profile',
                    href='/my/profile' ),
                  ( '#screens',
                    ( 'default', dict( path='page.user.profile' )))),
                ( 'objects', dict(
                    title="My Things",
                    href="/my" ),
                  ( '#screens',
                    ( 'default', dict(
                        path='dashboard.user.objects',
                        entry=dict(
                            data=dict(
                                source='userdata'
                            )
                        ))))),
                ( 'connections', dict(
                    title='My Connections',
                    href='/my/connections' ),
                  ( '#screens',
                    ( 'default', dict( path='dashboard.from_model' )))),
                ( 'settings', dict(
                    title='My Settings',
                    href='/my/settings' ),
                  ( '#screens',
                    ( 'default', dict( path='dashboard.from_model' )))),
                ( 'pages', dict(
                    title="My Pages",
                    href="/my/pages" ),
                  ( '#screens',
                    ( 'default', dict( path='view.collection' )))),
                ( 'groups', dict(
                    title='My Groups',
                    href='/my/groups' ),
                  ( '#screens',
                    ( 'default', dict( path='dashboard.from_model' )))),
                ( 'roles', dict(
                    title='My Roles',
                    href='/my/roles' ),
                  ( '#screens',
                    ( 'default', dict( path='dashboard.from_model' ))))),
              ( 'public', dict(
                  title='User Home Page',
                  href='/{user}' ),
                ( '#screens',
                  ( 'default',
                    dict( path='page.user.home' ))),
                ( 'profile', dict(
                    title='User Profile',
                    href='/{user}/profile' ),
                  ( '#screens',
                    ( 'default', dict( path='page.user.profile' )))),
                ( 'objects', dict(
                    title="User Stuff",
                    href="/{user}/stuff" ),
                  ( '#screens',
                    ( 'default', dict(
                        path='page.user.objects',
                        entry=dict(
                            data=dict(
                                source='userdata'
                            )))))),
                ( 'connections', dict(
                    title='User Connections',
                    href='/{user}/connections' ),
                  ( '#screens',
                    ( 'default', dict( path='dashboard.from_model' )))),
                ( 'settings', dict(
                    title='User Settings',
                    href='/{user}y/settings' ),
                  ( '#screens',
                    ( 'default', dict( path='dashboard.from_model' )))),
                ( 'pages', dict(
                    title="User Pages",
                    href="/{user}/pages" ),
                  ( '#screens',
                    ( 'default', dict( path='view.collection' )))),
                ( 'groups', dict(
                    title='User Groups',
                    href='/{user}/groups' ),
                  ( '#screens',
                    ( 'default', dict( path='dashboard.from_model' )))),
                ( 'roles', dict(
                    title='User Groups',
                    href='/{user}/groups' ),
                  ( '#screens',
                    ( 'default', dict( path='dashboard.from_model' )))),
              ))),
          ( '#settings',
            ( 'from relations', self.objects, self.relations ),
          ),
          ( '#containers',
            ( 'links.menu',
              ( 'user', dict(
                  title='User Menu',
                  description='Main User Menu'
              )),
              ( 'user_shortcuts', dict(
                  title='User Shortcuts Menu',
                  description='Main user linsk'
              )))),
          ( '#links',
            ( 'menu.user',
              ( 'home', dict(
                  title='My Home Page',
                  icon='fontawesome.home',
                  location='user.private' )),
              ( 'profile', dict(
                  title='My Profile',
                  icon='fontawesome.user-cog',
                  location='user.private.profile' )),
              ( 'things', dict(
                  title='My Stuff',
                  icon='fontawesome.dolly-flatbed',
                  location='user.private.objects' )),
              ( 'settings', dict(
                  title='Settings',
                  icon='fontawesome.cog',
                  location='user.private.settings' )),
              ( 'pages', dict(
                  title='My Pages',
                  icon='fontawesome.file-code',
                  location='user.private.pages' )),
              ( 'groups', dict(
                  title='My Groups',
                  icon='fontawesome.users',
                  location='user.private.groups' )),
              ( 'roles', dict(
                  title='My Roles',
                  icon='fontawesome.user-tie',
                  location='user.private.roles' )),
              # ( '', dict(
              #     title='',
              #     icon='fontawesome.',
              #     location='' )),
              ( '_shortcuts',
                ( 'home', dict(
                    title='My Home Page',
                    icon='fontawesome.home',
                    location='user.private' )),
                ( 'profile', dict(
                    title='My Profile',
                    icon='fontawesome.user-cog',
                    location='user.private.profile' )),
                ( 'things', dict(
                    title='My Stuff',
                    icon='fontawesome.dolly-flatbed',
                    location='user.private.objects' )),
                ( 'settings', dict(
                    title='Settings',
                    icon='fontawesome.cog',
                    location='user.private.settings' )),
                ( 'pages', dict(
                    title='My Pages',
                    icon='fontawesome.file-code',
                    location='user.private.pages' )),
              )),
          )
        ),
        ( '0.1.0',
          ( '#actions',
            ( 'connect-user', dict(
                icon='fontawesome-icon.user-plus',
                title='Connect',
                description='''Connect to another user.''',
                data=dict(
                    reverse='disconnect-user',
                    widget='Connector',
                )),
            ),
            ( 'disconnect-user', dict(
                icon='fontawesome-icon.user-minus',
                title='Disconnect',
                description='''Disconnect from a user.''',
                data=dict(
                    reverse='connect-user',
                    widget='Connector',
                )),
            ),
            ( 'block-user', dict(
                icon='fontawesome-icon.user-slash',
                title='Block User',
                description='''Block a user.

All connections between you will be de-activated. If you un-block the user later, any existing connections between you, you will be allowed to edit before the un-blocking is completed.''',
                data=dict(
                    reverse='unblock-user',
                    widget='Connector',
                )),
            ),
            ( 'unblock-user', dict(
                icon='fontawesome-icon.user-slash',
                title='Block User',
                description='''Un-block a user.

If there are any existing connections between you, you will be allowed to edit them before process is completed.''',
                data=dict(
                    reverse='block-user',
                    widget='Connector',
                )),
            ),
            ( 'report-user', dict(
                icon='fontawesome-icon.user-tag',
                title='Report User',
                description='''Report a user to the relevant authority.''',
                data=dict(
                    widget='Connector',
                )),
            ),
            ( 'invite-user', dict(
                icon='fontawesome-icon.id-card',
                title='Invite',
                description='''Send a link to a user to sign up to the site and become a connection.''',
                data=dict(
                    reverse='cancel-invite',
                    widget='Connector',
                )),
            ),
            ( 'cancel-invite', dict(
                icon='fontawesome-icon.comment-slash',
                title='Cancel Invite',
                description='''Cancer previously sent user invite.''',
                data=dict(
                    reverse='invite-user',
                    widget='Connector',
                )),
            ),
            ( 'confirm-connection', dict(
                icon='fontawesome-icon.user-check',
                title='Confirm',
                description='''Respond positively to a user connection and define your connection to the user.''',
                data=dict(
                    reverse='deny-connection',
                    widget='Connector',
                )),
            ),
            ( 'deny-connection', dict(
                icon='fontawesome-icon.user-times',
                title='Deny',
                description='''Reject a users claim to be connected to you, in the manner defined, implying no connection at all.''',
                data=dict(
                    reverse='confirm-connection',
                    widget='Connector',
                )),
            ),
            ( 'dispute-connection', dict(
                icon='fontawesome-icon.user-edit',
                title='Dispute',
                description='''Accept that a user is connected to you, but challenge the definition given.''',
                data=dict(
                    widget='Connector',
                )),
            ),
          )
        ),
        ( '0.1.1',
          ( '#links',
            ( 'menu.user',
              ( 'connections', dict(
                  title='My Connections',
                  icon='fontawesome.users',
                  location='user.private.connections' )),
              ( '_shortcuts',
                ( 'profile', dict(
                    title='My Connections',
                    icon='fontawesome.users',
                    location='user.private.connections' )),
            )),
          )
        ),
        ( '0.1.2',
          ( '#blocks',
            ( 'header.user.connections', dict(
                data=dict(
                    component='UserConnectionsHeader'
                ))),
          ),
          ( '#screens',
            ( 'dashboard',
              ( 'user', dict(
                  icon='fontawesome.user',
                  extends='dashboard',
                  data=dict(
                      component='UserDashboard',
                  )),
                ( 'connections', dict(
                    icon='fontawesome.cube',
                    extends='dashboard.sectional' ),
                  ( '#blocks',
                    ( 'primary',
                      dict(
                          path='viewer.objects',
                          entry=dict(
                              data=dict(
                                  mode='featured'
                              )))),
                    ( 'secondary',
                      dict(
                          path='viewer.objects',
                          entry=dict(
                              data=dict(
                                  mode='recent'
                              )))),
                    ( 'body', dict( path='viewer.objects' ))))
              )),
            ( 'page.user', dict(
                icon='fontawesome.home',
                data=dict(
                    component='UserPage',
                )),
              ( 'connections', dict(
                  icon='fontawesome.cube',
                  data=dict(
                      component='UserObjectsPage'
                  ))),
            )
          ),
          ( '#locations',
            ( 'user',
              ( 'private.connections', {},
                ( '#screens',
                  ( 'default', dict(
                      path='dashboard.user.connections',
                        entry=dict(
                            data=dict(
                                source='userconnections',
                                layout=dict(
                                    title='title',
                                    subtitle='subtitle',
                                    content='content'
                                ),
                                actions=(
                                    'connect-user',
                                    'disconnect-user',
                                    'block-user',
                                    'unblock-user',
                                    'report-user',
                                    'invite-user',
                                    'cancel-invite',
                                    'confirm-connection',
                                    'deny-connection',
                                    'dispute-connection',
                                ),
                                search='title subtitle content'.split()
                            ))),
                    ( '#blocks',
                      ( 'breakfront', dict( path='featured' )),
                      ( 'main', dict( path='grid.filtered' )))))),
              ( 'public.connections', {},
                ( '#screens',
                  ( 'default', dict(
                      path='dashboard.from_model',
                        entry=dict(
                            data=dict(
                                source='userconnections',
                                layout=dict(
                                    title='title',
                                    subtitle='subtitle',
                                    content='content'
                                ),
                                actions=(
                                    'connect-user',
                                    'disconnect-user',
                                    'block-user',
                                    'unblock-user',
                                    'report-user',
                                    'invite-user',
                                    'cancel-invite',
                                    'confirm-connection',
                                    'deny-connection',
                                    'dispute-connection',
                                ),
                                search='title subtitle content'.split()
                            ))),
                    ( '#blocks',
                      ( 'breakfront', dict( path='featured' )),
                      ( 'main', dict( path='grid.filtered' )))))),
            ))
        ),
        ( '0.1.3',
          ( '#create', 'userconnectiontype',
            ( dict( name='self' ), # LOL!
              dict(
                  title='Self',
                  display='Self',
              )),
            ( dict( name='friend' ),
              dict(
                  title='Friend',
                  display='Friend',
                  reverse=( '.', dict( name='self' ))
              )),
            ( dict( name='acquantance' ),
              dict(
                  title='Acquaintance',
                  display='Acquaintance',
                  reverse=( '.', dict( name='self' ))
              )),
            ( dict( name='colleague' ),
              dict(
                  title='Colleague',
                  display='Colleague',
                  reverse=( '.', dict( name='self' ))
              )),
            ( dict( name='brother' ),
              dict(
                  title='Brother',
                  display='Brother',
                  reverse=( '#create', '.',
                            ( dict( name='sibling' ),
                              dict(
                                  title='Sibling',
                                  display='Sibling',
                                  reverse=( '.', dict( name='self' ))
                              )))
              )),
            ( dict( name='sister' ),
              dict(
                  title='Sister',
                  display='Sister',
                  reverse=( '.', dict( name='sibling' ))
              )),
            ( dict( name='mother' ),
              dict(
                  title='Mother',
                  display='Mother',
                  reverse=( '#create', '.',
                            ( dict( name='child' ),
                              dict(
                                  title='Child',
                                  display='Child',
                                  reverse=( '#create', '.',
                                            ( dict( name='parent' ),
                                              dict(
                                                  title='Parent',
                                                  display='Parent',
                                              )))
                              )))
              )),
            ( dict( name='father' ),
              dict(
                  title='Father',
                  display='Father',
                  reverse=( '.', dict( name='child' ))
              )),
            ( dict( name='son' ),
              dict(
                  title='Son',
                  display='Son',
                  reverse=( '.', dict( name='parent' ))
              )),
            ( dict( name='daughter' ),
              dict(
                  title='Daughter',
                  display='Daughter',
                  reverse=( '.', dict( name='parent' ))
              )),
            ( dict( name='boyfriend' ),
              dict(
                  title='Boyfriend',
                  display='Boyfriend',
                  reverse=( '#create', '.',
                            ( dict( name='partner' ),
                              dict(
                                  title='Partner',
                                  display='Partner',
                                  reverse=( '.', dict( name='self' ))
                              )))
              )),
            ( dict( name='girlfriend' ),
              dict(
                  title='Girlfriend',
                  display='Girlfriend',
                  reverse=( '.', dict( name='partner' ))
              )),
            ( dict( name='fiancee' ),
              dict(
                  title='Fiancee',
                  display='Fiancee',
                  reverse=( '#create', '.',
                            ( dict( name='affianced' ),
                              dict(
                                  title='Affianced',
                                  display='Affianced',
                                  reverse=( '.', dict( name='self' ))
                              )))
              )),
            ( dict( name='fiance' ),
              dict(
                  title='Fiance',
                  display='Fiance',
                  reverse=( '.', dict( name='affianced' ))
              )),
            ( dict( name='husband' ),
              dict(
                  title='Husband',
                  display='Husband',
                  reverse=( '#create', '.',
                            ( dict( name='life-partner' ),
                              dict(
                                  title='Life Partner',
                                  display='Life Partner',
                                  reverse=( '.', dict( name='self' ))
                              )))
              )),
            ( dict( name='husband' ),
              dict(
                  title='Husband',
                  display='Husband',
                  reverse=( '.', dict( name='life-partner' ))
              )),
            ( dict( name='wife' ),
              dict(
                  title='Wife',
                  display='Wife',
                  reverse=( '.', dict( name='life-partner' ))
              )),
          )
        )
    )
    @property
    def userdata( self ):
        return ()
