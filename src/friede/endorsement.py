from .models import Endorsement
from .io import Request


def hashendorsement( endorsed ):
    return hash( str( endorsed )) # TODO: for now


class EndorsementProvider( object ):
    def __init__( self ):
        super( EndorsementProvider, self ).__init__()

    def endorse( self, endorsed, context=None, endorsement=None ):
        pass


class EndorsementManager( object ):
    registry = {}
    _sorted = ()

    def __init__( self ):
        super( EndorsementManager, self ).__init__()

    def add( self, endorser, priority=float( 'inf' )):
        self.registry[ endorser.name ] = ( endorser, priority )
        self._sorted = map( lambda x: x[0],
                            sorted( self.registry.values(),
                                    key=lambda x: x[1] ))

    def saveendorsement( self, endorsed, hash, context=None ):
        Endorsement.objects.create(
            hash=hash,
            endorsed=endorsed
        )

    def endorse( self, endorsed, hash, context=None ):
        result = EndorsementManager.getendorsement( hash, context=context )
        if result is not None:
            return result
        for endorser in self._sorted:
            result = endorser.endorse( endorsed, hash, context )
            if result is not None: # truthy = endorsed, falsy = forbidden
                if result:
                    self.saveendorsement( endorsed, hash, context )
                return result
        return None

    @staticmethod
    def getendorsement( hash, context=None ):
        try:
            return Endorsement.objects.get( hash=hash )
        except Endorsement.DoesNotExist:
            return None


class CacheEndorser( EndorsementProvider ):
    name = 'cache'

    def endorse( self, endorsed, hash, context=None ):
        hash = hashendorsement( endorsed )
        try:
            Endorsement.objects.get( hash=hash )
            return endorsed
        except Endorsement.DoesNotExist:
            return None


class EndorsementRequest( Request ):
    """EndorsementRequest differs from Request in that it maintains a relatively
    flat structure, and does the resolution of conflicts invisibly based on user
    selecions.
    """
    def __init__( self, endorsed, hash, context={} ):
        super( EndorsementRequest, self ).init(
            id="endorsement-{}".format( hash ),
            context=context )
        self.endorsement = ( endorsed, hash )

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
        pass


manager = EndorsementManager()
# manager.add( CacheEndorser(), float('-inf'))
