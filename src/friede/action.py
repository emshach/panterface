from collections import OrderedDict, deque
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from .exception import OperationRuntimeError, InvalidOperationError
from inspect import isclass
from .models import (
    Operation as OpModel,
    Action as ActModel,
    ActionStatus,
    OpStatus
)
from .util import Noop, getmodel
from .io import Request

actions = OrderedDict()
user_actions = OrderedDict()


def action(f):
    "decorator defining a class or function as a site action"
    r = actions
    if isinstance( f, type ):
        name = f.name
    else:
        name = f.__name__
        if name.startswith( 'user_' ):
            r = user_actions
            name = name[5:]
    r[ name ] = f
    return f


def dispatch( user, context={}, *ops ):
    op = Operation( user=user, context=context, ops=ops ) if len( ops ) > 1 \
        else Operation( user=user, **ops[0] )
    return op.run()             # friede.Response


def resume( user, op_id, context ):
    op = Operation( user, op_id )
    return op.resume( context )


class OpList( list ):
    def __repr__( self ):
        return "{}({})".format(
            self.__class__.__name__,
            super( OpList, self ).__repr__()
        )


class AnyOf( OpList ):
    pass


class SomeOf( OpList ):
    pass


class AllOf( OpList ):
    pass


class NoneOf( OpList ):
    pass


class NotAllOf( OpList ):
    pass


class Action( object ):
    name = None
    permname = None

    def __init__( self, op=None, object=None, **kw ):
        super( Action, self ).__init__()
        self.object = object
        self.op = op

    def __eq__( self, other ):
        return type( self ) == type( other )\
            and self.object == other.object

    def run( self, **kw ):
        pass

    def getuser( self ):
        pass

    def getneeds( self, context, **kw ):
        return ()

    @property
    def model( self ):
        return ActModel.objects.get( path="actions.{}".format( self.name ))

    @staticmethod
    def get_for_object( object ):
        name = object.path
        if name.startswith( 'actions.' ):
            name = name[ 8: ]
        return actions[ name ]

    @staticmethod
    def getaction( action ):
        actionclass = None
        actionobj = None
        if not action:
            return None, None, None
        if isinstance( action, basestring ):
            try:
                action = ActModel.objects.get( name=action )
                actionobj = None
            except ActModel.DoesNotExist:
                return None, None, None
        elif isinstance( action, int ):
            try:
                action = ActModel.objects.get( pk=action )
                actionobj = None
            except ActModel.DoesNotExist:
                return None, None, None
        elif isinstance( action, Action ):
            return actionobj.model, action.__class__, action
        elif isclass( action ) and issubclass( action, Action ):
            actionclass = action
            action = None
        else:
            return None, None, None
        if not isclass( actionclass ) or not issubclass( actionclass, Action ):
            if not action:
                return None, None, None
            return action, Action.get_for_object( action ), None


class MemoEntry( object ):
    def __init__( self, needs=None, cond=None, requests=None ):
        self.needs = needs or []
        self.cond = cond or []
        self.requests = requests or []


class DependencyMemo( OrderedDict ):
    def entry( self, key ):
        if key not in self:
            self[ key ] = MemoEntry()
        return self[ key ]


class MatchType:
    CEDE     = 'Cedes'
    EQUAL    = 'Equals'
    SATISFY  = 'Satisfies'
    CONFLICT = 'Conflicts'
    DEPEND   = 'Depends'
    SUPPORT  = 'Supports'


class DependencyManager( object ):

    def __init__( self, root, requests=[] ):
        super( DependencyManager, self ).__init__()
        self.root = root
        self.cond = []
        self.needs = []
        self.new = deque([])
        self.memo = DependencyMemo()
        self._requests = requests
        if self.needs:
            self.memo.entry( root.pk ).needs.extend( self.needs )

    def __nonzero__( self ):
        return True

    def __hash__( self ):
        return id( self )

    def addcond( self, action, obj ):
        pass

    def addconds( self, action, objs ):
        pass

    def addneed( self, action, obj ):
        op = action.op
        need = None
        for n in self.needs:
            val = n.compare( obj )
            if val:
                if val == MatchType.CONFLICT:
                    raise InvalidOperationError(
                        'Conflicting dependencies', n, obj )
                elif val == MatchType.EQUAL:
                    return n
                elif val == MatchType.SATISFY:
                    need = Operation( **obj )
                    n.covers( need )
                    break
                elif val == MatchType.CEDE:
                    need = Operation( **obj )
                    need.covers(n)
                    break
        else:
            need = Operation( **obj )
        self.memo.entry( op.pk ).needs.push( need )
        return need

    def addneeds( self, action, objs ):
        # account for list type (any, all etc)
        pass

    def addrequest( self, action, obj ):
        op = action.op
        for i, q in enumerate( self.requests ):
            val = q.compare( obj )
            if val:
                if val in ( MatchType.EQUAL, MatchType.SATISFY ):
                    return q
                elif val == MatchType.CEDE:
                    request = Question( **obj )
                    self._requests.pop(i)
                    self._requests.insert( i, request )
                    self.memo[ request ] = action.op
                    self.memo.entry( op.pk ).requests.push( request )
                    self.memo.pop( q, None )
                    return request
        request = Question( **obj )
        self._requests.push( request )
        self.memo[ request ] = action.op
        self.memo.entry( op.pk ).requests.push( request )
        return request

    @property
    def unmet( self ):
        return ()
        # return filter( lambda x: x.unmet and not x.satisfied_by, self.needs )

    @property
    def primary( self ):
        return filter( lambda x: not x.blocked, self.needs )

    @property
    def requests( self ):
        stack = deque([ self.root ])
        requests = []
        memo = {}
        while stack:
            op = stack.popleft()
            if op.pk in memo:
                continue
            memo[ op.pk ] = op
            if not op.done:
                print 'memo', self.memo
                if self.memo.get( op.pk ) and self.memo[ op.pk ].requests:
                    requests.extend( self.memo[ op.pk ].requests )
                # unmet = op.unmet
                # if unmet:
                #     stack.extend( unmet )
                if op.children:
                    stack.extend( op.children )
        return requests


class OperationContext( dict ):
    def __init__( self, op, *arg, **kw ):
        super( OperationContext, self ).__init__( *arg, **kw )
        self.deps = DependencyManager( root=op )

    def __nonzero__( self ):
        return True

    def addcond( self, action, obj ):
        return self.deps.addcond( action, obj )

    def addconds( self, action, objs ):
        return self.deps.addconds( action, objs )

    def addneed( self, action, obj ):
        return self.deps.addneed( action, obj )

    def addneeds( self, action, objs ):
        return self.deps.addneeds( action, objs )

    def addrequest( self, action, obj ):
        return self.deps.addrequest( action, obj )


class Question( dict ):
    def __init__( self, *arg, **kw ):
        super( Question, self ).__init__( *arg, **kw )

    def sameas( self, data ):
        pass


class Operation( object ):
    def __nonzero__( self ):
        return True

    def __init__( self, user, parent=None, child=None, action=None,
                  model=None, id=None, ids=(), object=None, ops=None,
                  store=None, arg=(), kw={} ):
        super( Operation, self ).__init__()
        self.arg = arg
        self.kw = kw
        self.store = Noop()
        if store:
            if isinstance( store, int ):
                store = OpModel.objects.get( pk=store )
            if user != store.user:
                raise InvalidOperationError(
                    'Trying to resume operation with different user',
                    store, user )
            model = getmodel( store.model )
            self.store = store
            self.object = store.object
            self.objects = ()
            if model and store.object_ids:
                self.objects = tuple( model.objects.filter(
                    pk__in=store.object_ids ))
            elif self.object:
                self.objects = ( self.object, )
            if self.action:
                self.actionclass = Action.get_for_object( self.action )
                self.actionobj = self.actionclass(
                    op=self,
                    object=self.object
                )
            self.status = store.status
            if store.context:
                if 'arg' in store.context:
                    self.arg = store.context[ 'arg' ]
                if 'kw' in store.context:
                    self.kw = store.context[ 'kw' ]
            if parent:
                self.parent = parent
            elif store.parent:
                self.parent = Operation( user, store=store.parent, child=self )
            else:
                self.parent = None
            if store.children:
                self.children = tuple(
                    o if child.store is o
                    else Operation( user, parent=self, store=o )
                    for o in store.children.all()
                ) if child else tuple(
                    Operation( user, parent=self, store=o )
                    for o in store.children.all()
                )
            return

        if ids and len( ids ) == 1:
            ( id, ) = ids
            ids = ()
        status = None
        actionclass = None
        actionobj = None
        self.parent = parent
        self.objects = ()
        self.object = object
        self.actionclass = None
        error = None
        try:
            # action
            if action:
                a = action
                action, actionclass, actionobj = Action.getaction(a)
                if action is None:
                    if not isinstance( a, ( Action, basestring, int )):
                        if not isclass(a) or not issubclass( a, Action ):
                            raise InvalidOperationError( 'Invalid action', a )
                        raise InvalidOperationError(
                            'Action wrong type', type(a))
                    if not isclass( actionclass )\
                       or issubclass( actionclass, Action ):
                        raise InvalidOperationError( 'Invalid action', a )
                    raise InvalidOperationError( 'Action not found', a )
            # object
            if model:
                model = getmodel( model )
            else:
                model = self.getmodel()
            if not object and model:
                if id:
                    try:
                        self.object = model.objects.get( pk=id )
                        self.objects = ( self.object, )
                    except model.DoesNotExist:
                        raise InvalidOperationError(
                            'Object not found', model, id )
                elif ids:
                    objects = tuple( model.objects.filter( pk__in=ids ))
                    if len( objects ) < len( set( ids )):
                        raise InvalidOperationError(
                            'Some objects not found', model, ids )
                    self.objects = objects

            self.actionclass = actionclass
            actionclass = self.getactionclass()
            if not actionobj and actionclass and self.object:
                actionobj = actionclass( op=self, object=self.getobject() )
                action = actionobj.model
            self.actionobj = actionobj
        except InvalidOperationError as e:
            status = dict(
                type='invalid_operation',
                message=str(e),
                data=e.data
            )
            error = e
        if status is None:
            status = dict(
                type='init'
            )
        self.store = OpModel.objects.create(
            user=user,
            parent=parent.store if parent else None,
            action=action,
            model=( ContentType.objects.get_for_model( model ) if model
                    else None ),
            object_id=id,
            object_ids=ids,
            ops=ops,
            context=dict(
                arg=self.arg,
                kw=self.kw
            )
        )
        OpStatus.objects.create(
            status=ActionStatus.get( status[ 'type' ]),
            message=status.get( 'message' ),
            data=status.get( 'data', {} ),
            operation=self.store
        )
        if error:
            raise error
        objects = self.getobjects()

        self.children = (
            tuple(
                Operation( user, parent=self, object=o )
                for o in objects
            ) if len( objects ) > 1 and actionclass
            else () ) + ( tuple(
                Operation( user, parent=self, **o ) for o in ops
            ) if ops else () )

    def run( self, context=None, **kw ):
        import pprint
        print 'running op'
        pprint.pprint(  self.__dict__ )
        if self.done:
            return self.status  # TODO: maybe warn
        if context is None:
            context = OperationContext( self )
        elif isinstance( context, dict ):
            context = OperationContext( self, **context )
        needs, requests = self.getneeds( context, **kw )
        if requests:
            return requests
        stack = deque( context.deps.primary )
        while stack:
            op = stack.popleft()
            status = op.runwith( context, **kw )
            if isinstance( status, Question ):
                return status
            if not Operation.ok( status ):
                return OpStatus.objects.create(
                    status=ActionStatus.get( 'failed' ),
                    message='Failed to meet operation prerequisites',
                    operation=self.store
                )
            push = []
            # for n in op.dependents:
            #     n.unmet.remove( op )
            #     if not len( n.unmet ):
            #         push.push(n)
            stack.extendleft( push[ ::-1 ])
        return self.runwith( context )

    def runwith( self, context, **kw ):
        if self.done:
            return self.status  # TODO: maybe warn
        status = None
        if self.children:
            aborted = ActionStatus.get( 'parent_aborted' )
            i = 0
            for o in self.children:
                _status = o.status if o.done and Operation.ok( o.status )\
                    else o.runwith( context, **kw )
                if isinstance( _status, Question ):
                    return _status
                if not Operation.ok( _status ):
                    for c in self.children[( i + 1 ): ]:
                        _status = OpStatus.objects.create(
                            status=aborted,
                            message='Preceding operation in set failed',
                            operation=c.store
                        )
                    failed = ActionStatus.get( 'failed' )
                    status = OpStatus.objects.create(
                        status=failed,
                        message='Operation failed',
                        operation=self.store
                    )
                    return status
                i += 1
            if self.actionobj:
                status = self.actionobj.run( context, **kw )
        elif self.actionobj:
            status = self.actionobj.run( context, **kw )
        else:
            raise OperationRuntimeError( "action and/or children" )
            # TODO: incorporate into op flow

        if not status:
            success = ActionStatus.get( 'success' )
            status = OpStatus.objects.create(
                status=success,
                message='Operation completed successfully',
                operation=self.store
            )
            self.done = now()
        elif Operation.ok( status ):
            self.done = now()
        return status

    def resume( self, context=None, **kw ):
        return self.run( context, **kw )

    def save( self ):
        return self.store.save()

    def getneeds( self, context, **kw ):
        if self.actionobj:
            needs, unmet, requests = self.actionobj.getneeds( context, **kw )
        elif self.children:
            for c in self.children:
                c.getneeds( context, **kw )
        return context.deps.needs, context.deps.requests

    def getactionclass( self ):
        return self.actionclass \
            or ( self.parent and self.parent.getactionclass() )

    def getactionobj( self ):
        return self.actionobj or ( self.parent and self.parent.getactionobj() )

    def getmodel( self ):
        return self.model or ( self.parent and self.parent.getmodel() )

    def getobject( self ):
        return self.object or ( self.parent and self.parent.getobject() )

    def getobjects( self ):
        return self.objects or ( self.parent and self.parent.getobjects() )

    def covers( self, op ):
        self.store.satisfies.add( op )

    def compare( self, data ):
        if self.actionobj:
            return self.actionobj.compare( data )
        # TODO: and more complex ops?

    @staticmethod
    def ok( self, status, statuses=() ):
        if status:
            return bool( status.status )
        if statuses:
            return all( s.status for s in statuses )
        return False

    # store proxy getter/setters

    @property
    def pk( self ):
        return self.store.pk

    @property
    def user( self ):
        return self.store.user

    @user.setter
    def user( self, user ):
        self.store.user = user
        self.store.save()

    @property
    def action( self ):
        return self.store.action

    @action.setter
    def action( self, action ):
        self.store.action = action
        self.store.save()

    @property
    def model( self ):
        return self.store.model

    @model.setter
    def model( self, model ):
        self.store.model = model
        self.store.save()

    # @property
    # def context( self ):
    #     return self.store.context

    # @context.setter
    # def context( self, context ):
    #     self.store.context = context
    #     self.store.save()

    @property
    def status( self ):
        return self.store.status

    @status.setter
    def status( self, status ):
        self.store.status = status
        self.store.save()

    @property
    def object_id( self ):
        return self.store.object_id

    @object_id.setter
    def object_id( self, object_id ):
        self.store.object_id = object_id
        self.store.save()

    @property
    def object_ids( self ):
        return self.store.object_ids

    @object_ids.setter
    def object_ids( self, object_ids ):
        self.store.object_ids = object_ids
        self.store.save()

    @property
    def ops( self ):
        return self.store.ops

    @ops.setter
    def ops( self, ops ):
        self.store.ops = ops
        self.store.save()

    # @property
    # def dryrun_ok( self ):
    #     return self.store.dryrun_ok

    # @dryrun_ok.setter
    # def dryrun_ok( self, dryrun_ok ):
    #     self.store.dryrun_ok = dryrun_ok
    #     self.store.save()

    @property
    def done( self ):
        return self.store.done

    @done.setter
    def done( self, done ):
        self.store.done = done
        self.store.save()

    @property
    def satisfies( self ):
        return self.store.satisfies.all()

    @satisfies.setter
    def satisfies( self, satisfies ):
        self.store.satisfies.clear()
        self.store.satisfies.add( *satisfies )
        self.store.save()

    @property
    def satisfied_by( self ):
        return self.store.satisfied_by.all()

    @satisfied_by.setter
    def satisfied_by( self, satisfied_by ):
        self.store.satisfied_by.clear()
        self.store.satisfied_by.add( *satisfied_by )
        self.store.save()

    # calculated attributes
    @property
    def blocked( self ):
        return not self.store.unmet.count() and not self.satisfied_by


class ActionRequest( Request ):
    """AcitonRequest differs from Request in that it maintains a relatively flat
    structure, and does the resolution of conflicts invisibly based on user
    selecions.
    """
    def __init__( self, id, body=[], context={} ):
        super( ActionRequest, self ).init( id=id, body=body, context=context )

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
