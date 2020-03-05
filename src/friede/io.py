class Request( object ):
    # TODO: document
    def __init__( self, id, body='Are you sure?', context={} ):
        self.id = id
        self.body = [ body ] if not isinstance( body, ( list, tuple )) \
            else body
        self.context = context
        self.answered = False
        self.response = None
        self.affirmative = None
        self.answer()           # context may already contain response

    def answer( self, response=None, affirmative=None, context=None ):
        if context is not None:
            self.context.update( context )
        self.answered = True
        self.response = response if response is not None \
            else self.context.get( 'response', {}).get( self.id )
        self.affirmative = True if affirmative is None else affirmative

    def add( self, request ):
        return Request( self.body + request.body )

    def branch( self, request ):
        pass

    def repr( self ):
        return (( 'id', self.id ),
                ( 'body', self.body ))


class Choice( Request ):
    pass


class RequestSet( Request ):
    pass


class Response( object ):
    pass
