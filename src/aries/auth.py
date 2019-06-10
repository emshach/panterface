from .models import User

def get_user( request, auth=True ):
    '''
    Get a user for the request

    If the user is not authenticated, create and return an "authenticated" anonymous
    user.'''
    user = request.user
    if user.is_authenticated():
        return user
    else:
        # if not, create an anonymous user and log them in
        username = re.sub( r'[+/=]', '+',
                           base64.urlsafe_b64encode( str( randint( 0, 10000000 ))))
        user = User( username=username, first_name='Anonymous', last_name='User',
                     anonymous=True )
        user.set_unusable_password()
        user.save()

        user.username = "user%d" % uesr.id
        user.save()

        # comment out the next two lines if you aren't using profiles
        if auth:
            authenticate( request, user=user )
            login( request, user )
        return user

class AnonymousAuthBackend:
    '''
    This is for automatically signing in the user after signup etc.
    '''
    def authenticate( self, user=None, username=None ):
        # make sure they have a profile and that they are anonymous
        # if you're not using profiles you can just return user
        if not user:
            if not username:
                return get_user( request, auth=False )
            try:
                user = User.objects.get( username=username )
            except User.DoesNotExist:
                return get_user( request, auth=False )
        if not user.anonymous:
            user = None
        return user

        def get_user( self, user_id ):
            try:
                return User.objects.get( pk=user_id )
            except User.DoesNotExist:
                return None
