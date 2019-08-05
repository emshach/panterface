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

    objects = 'user group policy permission role'.split()

    min_version = '0.0.1'
    required = True
    user_required = True

    relations = dict(
        user={
            'model'  : 'User',
            'icon'   : 'fontawesome.',
            'plural' : 'users',
            'has'    : (),
            'in'     : (),
            'links'  : (),
        },
        group={
            'model'  : 'Group',
            'icon'   : 'fontawesome.',
            'plural' : 'groups',
            'has'    : (),
            'in'     : (),
            'links'  : (),
        },
        policy={
            'model'  : 'Policy',
            'icon'   : 'fontawesome.',
            'plural' : 'policies',
            'has'    : (),
            'in'     : (),
            'links'  : (),
        },
        permission={
            'model'  : 'Permission',
            'icon'   : 'fontawesome.',
            'plural' : 'permissions',
            'has'    : (),
            'in'     : (),
            'links'  : (),
        },
        role={
            'model'  : 'Role',
            'icon'   : 'fontawesome.',
            'plural' : 'roles',
            'has'    : (),
            'in'     : (),
            'links'  : (),
        },
    )
    api=(
        ( r'can/(?P<perm>.+$)',  ( views.api_can,         'can', [ 'any' ])),
        ( r'can/?$',             ( views.api_which_can,   'which_can'     )),
        ( r'login/?$',           ( views.api_login,       'login'         )),
        ( r'logout/?$',          ( views.api_logout,      'logout'        )),
        ( r'register/?$',        ( views.api_register,    'register'      )),
        ( r'auth-status/?$',     ( views.api_auth_status, 'auth-status'   )),
    )
    routes=(
        ( 'users',       views.UserViewSet       ),
        ( 'groups',      views.GroupViewSet      ),
        ( 'policies',    views.PolicyViewSet     ),
        ( 'permissions', views.PermissionViewSet ),
        ( 'roles',       views.RoleViewSet       ),
    )
    serializers=(
        ( 'users',       serializers.UserSerializer       ),
        ( 'groups',      serializers.GroupSerializer      ),
        ( 'policies',    serializers.PolicySerializer     ),
        ( 'permissions', serializers.PermissionSerializer ),
        ( 'roles',       serializers.RoleSerializer       ),
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
              )),
            ( 'page.user', dict(
                icon='fontawesome.house',
                data=dict(
                    component='UserPage',
                )),
              ( 'home', dict(
                  icon='fontawesome.house',
                  data=dict(
                      component='UserHomePage',
                  ))),
              ( 'profile', dict(
                  icon='fontawesome.house',
                  data=dict(
                      component='UserProfilePage',
                  )),
              )
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
                    ( 'default', dict( path='dashboard.from_model' )))),
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
                    title='My Groups',
                    href='/my/groups' ),
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
                    ( 'default', dict( path='dashboard.from_model' )))),
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
                  title='User Home Page',
                  icon='fontawesome.home',
                  location='user.private' )),
              ( 'profile', dict(
                  title='Profile Page',
                  icon='fontawesome.user-cog',
                  location='user.private.profile' )),
              ( 'things', dict(
                  title='Stuff',
                  icon='fontawesome.dolly-flatbed',
                  location='user.private.objects' )),
              ( 'settings', dict(
                  title='Settings',
                  icon='fontawesome.cog',
                  location='user.private.settings' )),
              ( 'pages', dict(
                  title='Pages',
                  icon='fontawesome.file-code',
                  location='user.private.pages' )),
              ( 'groups', dict(
                  title='Groups',
                  icon='fontawesome.users',
                  location='user.private.groups' )),
              ( 'roles', dict(
                  title='Roles',
                  icon='fontawesome.user-tie',
                  location='user.private.roles' )),
              # ( '', dict(
              #     title='',
              #     icon='fontawesome.',
              #     location='' )),
              ( '_shortcuts',
              ( 'home', dict(
                  title='User Home Page',
                  icon='fontawesome.home',
                  location='user.private' )),
              ( 'profile', dict(
                  title='Profile Page',
                  icon='fontawesome.user-cog',
                  location='user.private.profile' )),
              ( 'things', dict(
                  title='Stuff',
                  icon='fontawesome.dolly-flatbed',
                  location='user.private.objects' )),
              ( 'settings', dict(
                  title='Settings',
                  icon='fontawesome.cog',
                  location='user.private.settings' )),
              ( 'pages', dict(
                  title='Pages',
                  icon='fontawesome.file-code',
                  location='user.private.pages' )),
            )),
          )
        ),
        # ( '0.1.0',
        #   ( '#widgets',
        #     ( 'help',
        #       ( 'list', dict(
        #           icon='fontawesome.list',
        #           data=dict(
        #               component='ActionHelpWidget',
        #               action='list'
        #           ))),
        #     ),
        #     ( 'dashboard', dict (
        #         icon='fontawesome.expand',
        #         data=dict(
        #             component='DashboardWidget'
        #         ))),
        #     ( 'from relations', self.objects, self.relations )),
        #   ( '#blocks',
        #     ( 'form',
        #       ( 'group', dict(
        #           icon='fontawesome.object-group',
        #           data=dict(
        #               component='FormGroup'
        #           ))),
        #     )),
        #   ( '#screens',
        #     ( 'form.single', dict(
        #         icon='fontawesome.file-alt',
        #         data=dict(
        #             component='FormPage'
        #         ))),
        #   ),
        # ),
    )
    @property
    def userdata( self ):
        return ()
