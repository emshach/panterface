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
        # ( '0.1.0',
        #   ( '#actions',
        #     ( 'list', dict(
        #         icon='fontawesome.list',
        #         title='List Object Data in Table Form',
        #         description='''''',
        #         data=dict(
        #             reverse='uninstall',
        #             widget='Installer',
        #         ))),
        #   ),
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
        #   ( '#locations',
        #     ( 'user',
        #       ( 'private', dict(
        #           title='My Page',
        #           href='/me' ),
        #         ( '#screens',
        #           ( 'default', dict( path='dashboard.user.home' )))),
        #       ( 'public', dict(
        #           title='User Profile',
        #           href='/{user}' ),
        #         ( '#screens',
        #           ( 'default', dict( path='dashboard.user' ))))),
        #     ( 'from relations', self.objects, self.relations )),
        #   ( '#settings',
        #     ( 'from relations', self.objects, self.relations ),
        #   ),
        #   ( '#containers',
        #     ( 'links.menu',
        #       ( 'user', dict(
        #           title='User Menu',
        #           description='Main User Menu'
        #       )))),
        #   ( '#links',
        #     ( 'menu.user',
        #       ( 'home', dict(
        #           title='User Home Page',
        #           icon='fontawesome.home',
        #           location='home' )),
        #       ( 'profile', dict(
        #           title='Profile Page',
        #           icon='fontawesome.user-cog',
        #           location='apps' )),
        #     )),
        # ),
    )
    @property
    def userdata( self ):
        return ()
