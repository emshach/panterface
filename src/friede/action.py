from collections import OrderedDict, deque
from django.utils.timezone import now
from .models import Operation as OpModel, Action as ActModel, ActionStatus, OpStatus

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


class Action( object ):
    name = None
    permname = None

    def __init__( self, op=Nonex, object=None, **kw ):
        super( Action, self ).__init__()
        self.object = object
        self.op = op

    def run( self, system=None, **kw ):
        if system == True:
            reqs = self.systemreqs()
            if self.op.met( reqs ):
                return self.runsystem( **kw )
            else:
                return ActionStatus.get( 'unmet_requirements' ), reqs
        elif system == False:
            reqs = self.userreqs()
            if self.op.met( reqs ):
                return self.runuser( **kw )
            else:
                return ActionStatus.get( 'unmet_requirements' ), reqs
        else:
            sysreqs = self.sysreqs()
            userreqs = self.userreqs()
            if self.op.met( sysreqs ):
                return self.runsystem( **kw )
            elif self.op.met( userreqs ):
                return self.runuser( **kw )
            else:
                return ActionStatus.get( 'unmet_requirements' ), dict(
                    user=userreqs,
                    system=systemreqs,
                )

    def dryrun( self, system=None, **kw ):
        if system == True:
            reqs = self.systemreqs()
            if self.op.met( reqs ):
                return self.dryrunsystem( **kw )
            else:
                return ActionStatus.get( 'unmet_requirements' ), reqs
        elif system == False:
            reqs = self.userreqs()
            user = self.getuser or self.op.user
            if self.op.met( reqs ):
                return self.dryrunuser( user=user, **kw )
            else:
                return ActionStatus.get( 'unmet_requirements' ), reqs
        else:
            sysreqs = self.sysreqs()
            userreqs = self.userreqs()
            if self.op.met( sysreqs ):
                return self.dryrunsystem( **kw )
            elif self.op.met( userreqs ):
                user = self.getuser or self.op.user
                return self.dryrunuser( user=user, **kw )
            else:
                return ActionStatus.get( 'unmet_requirements' ), dict(
                    user=userreqs,
                    system=systemreqs,
                )

    def runsystem( self, **kw ):
        return ActionStatus.get( 'not_implemented' ), ()

    def dryrunsystem( self, **kw ):
        return ActionStatus.get( 'not_implemented' ), ()

    def runuser( self, **kw ):
        return ActionStatus.get( 'not_implemented' ), ()

    def dryrunuser( self, **kw ):
        return ActionStatus.get( 'not_implemented' ), ()

    def getuser( self ): pass

    def requirements( self ):
        perm = permname if permname else name
        return ()

    def systemreqs( self ):
        return self.requirements()

    def systemreqset( self ):
        return self.systemreqs()

    def userreqs( self ):
        return self.requirements()

    def userreqset( self ):
        return self.userreqs()

    @staticmethod
    def get_for_object( obj ):
        pass


class DependencyManager( object ):
    def __init__( self ):
        super( self, DependencyManager ).__init__()
        self.primary = OrderedDict()
        self.all = OrderedDict()
        self.unmet = OrderedDict()

    def __nonzero__( self ): return True

class OperationContext( dict ):
    def __init__( self, *arg, **kw ):
        super( self, OpMemo ).__init__( *arg, **kw )
        self.needs = None

    def __nonzero__( self ): return True

    def initneeds( self ):
        self.needs = DependencyManager()


class Operation( object ):
    def __nonzero__( self ): return True

    def __init__( self, user, parent=None, child=None, action=None,
              model=None, id=None, ids=(), object=None, ops=None, store=None ):
        super( Operation, self ).__init__()
        if store:
            if isinstance( store, int ):
                store = OpModel.objects.get( pk=store )
            if user != store.user:
                raise InvalidOperationError(
                    'Trying to resume operation with different user',
                    store, user )
            self.store = store
            if self.action:
                self.actionclass = Action.get_for_object( self.action )
                self.actionobj = self.actionclass(
                    op=self,
                    object=self.action.object
                )
            self.status = store.status
            if parent:
                self.parent = parent
            elif store.parent:
                self.parent = Operation( user, store=store.parent, child=self )
            if store.children:
                self.children = tuple(
                    o if child.store is o
                    else Operation( user, parent=self, store=o )
                    for o in store.children
                ) if child else tuple(
                    Operation( user, parent=self, store=o )
                    for o in store.children
                )
            return

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
                if isinstance( action, basestring ):
                    try:
                        action = ActModel.objects.get( name=action )
                        actionobj = None
                    except ActModel.DoesNotExist:
                        raise InvalidOperationError( 'Action not found', action )
                elif isinstance( action, int ):
                    try:
                        action = ActModel.objects.get( pk=action )
                        actionobj = None
                    except ActModel.DoesNotExist:
                        raise InvalidOperationError( 'Action not found', action )
                elif isinstance( action, Action ):
                    actionclass = action.__class__
                    actionobj = action
                    action = actionobj.model
                elif issubclass( action, Action ):
                    actionclass = action
                    action = None
                else:
                    raise InvalidOperationError( 'Action wrong type', type( action ))
                if not issubclass( actionclass, Action ):
                    if not action:
                        raise InvalidOperationError( 'Invalid action', action )
                    actionclass = Action.get_for_object( action )
            # object
            model = self.getmodel()
            if not object and model:
                if id:
                    try:
                        self.object = model.get( pk=id )
                        self.objects = ( self.object, )
                    except model.DoesNotExist:
                        raise InvalidOperationError(
                            'Object not found', model, id )
                elif ids:
                    objects = tuple( model.filter( pk__in=ids ))
                    if len( objects ) < len( set( ids )):
                        raise InvalidOperationError(
                            'Some objects not found', model, ids )
                    self.objects = objects

            self.actionclass = actionclass
            actionclass = self.getactionclass()
            if not action and actionclass and self.object :
                action = actionclass( op=self, object=self.getobject() )
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
            parent=parent,
            action=action,
            model=model,
            object_id=id,
            object_ids=ids,
            ops=ops
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
            ) if objects and actionclass\
              else () )
        + ( tuple(
            Operation( user, parent=self, **o )
            for o in ops
        ) if ops else () )

    def dryrun( self, context, **kw ):
        if self.dryrun_ok:
            if pushed:
                self.popcontext()
                pushed = False
            return self.status
        status = None
        statuses = []
        if self.children:
            for o in self.children:
                _status = o.dryrun( context=context, **kw )
                statuses.push( _status )
            if self.actionobj:
                status = a.dryrun( **kw )
        elif self.actionobj:
            status = a.dryrun( **kw )
        else:
            raise OperationRuntimeError( "action and/or children" )
            # TODO: incorporate into op flow

        if Operation.ok( status, statuses ):
            if not status:
                success = ActionStatus.get( 'success' )
                status = OpStatus.objects.create(
                    status=success,
                    message='Operation completed successfully',
                    operation=self.store
                )
            self.dryrun_ok = now()
        elif not status:
            failed = ActionStatus.get( 'failed' )
            status = OpStatus.objects.create(
                status=failed,
                message='Operation failed',
                operation=self.store
            )
        if pushed:
            self.popcontext()
            pushed = False
        return status

    def run( self, context, **kw ):
        if self.done:
            return self.status  # TODO: maybe warn
        toplevel = not context.needs
        if toplevel:
            context.initneeds()
            needs, unmet = self.getneeds( context )
        status = None
        if not self.dryrun_ok:
            status = self.dryrun( context, **kw )
            if not Operation.ok( status ):
                return status
            status = None
        if self.children:
            aborted = ActionStatus.get( 'parent_aborted' )
            i = 0
            for o in self.children:
                _status = o.status if o.done and Operation.ok( o.status )\
                    else o.run( context, **kw )
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
                status = a.run( **kw )
        elif self.actionobj:
            status = a.run( **kw )
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

    def resume( self, context, **kw ):
        return self.run( context, **kw )

    # def pushcontext( context ):
    #     if not context:
    #         return False
    #     self.contextstack.push( dict( self.getcontext(), **context ))
    #     return True

    def save( self ):
        return self.store.save()

    # def getcontext( self ):
    #     return dict( self.parent and self.parent.getcontext() or {},
    #                  **( self.context or {} ))

    def getactionclass( self ):
        return self.actionclass or ( self.parent and self.parent.getactionclass() )

    def getactionobj( self ):
        return self.actionobj or ( self.parent and self.parent.getactionobj() )

    def getmodel( self ):
        return self.model or ( self.parent and self.parent.getmodel() )

    def getobject( self ):
        return self.object or ( self.parent and self.parent.getobject() )

    def getobjects( self ):
        return self.objects or ( self.parent and self.parent.getobjects() )

    @staticmethod
    def ok( self, status, statuses=() ):
        if status:
            return bool( status.status )
        if statuses:
            return all( s.status for s in statuses )
        return False

    # store proxy getter/setters

    @property
    def user( self, user ):
        return self.store.user

    @user.setter
    def user( self, user ):
        self.store.user = user
        self.store.save()

    @property
    def action( self, action ):
        return self.store.action

    @action.setter
    def action( self, action ):
        self.store.action = action
        self.store.save()

    @property
    def model( self, model ):
        return self.store.model

    @model.setter
    def model( self, model ):
        self.store.model = model
        self.store.save()

    # @property
    # def context( self, context ):
    #     return self.store.context

    # @context.setter
    # def context( self, context ):
    #     self.store.context = context
    #     self.store.save()

    @property
    def status( self, status ):
        return self.store.status

    @status.setter
    def status( self, status ):
        self.store.status = status
        self.store.save()

    @property
    def object_id( self, object_id ):
        return self.store.object_id

    @object_id.setter
    def object_id( self, object_id ):
        self.store.object_id = object_id
        self.store.save()

    @property
    def object_ids( self, object_ids ):
        return self.store.object_ids

    @object_ids.setter
    def object_ids( self, object_ids ):
        self.store.object_ids = object_ids
        self.store.save()

    @property
    def ops( self, ops ):
        return self.store.ops

    @ops.setter
    def ops( self, ops ):
        self.store.ops = ops
        self.store.save()

    @property
    def dryrun_ok( self, dryrun_ok ):
        return self.store.dryrun_ok

    @dryrun_ok.setter
    def dryrun_ok( self, dryrun_ok ):
        self.store.dryrun_ok = dryrun_ok
        self.store.save()

    @property
    def done( self, done ):
        return self.store.done

    @done.setter
    def done( self, done ):
        self.store.done = done
        self.store.save()

