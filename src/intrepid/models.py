# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.utils.encoding import python_2_unicode_compatible
from django.db import models as M
from django.contrib.postgres.fields import JSONField
from datetime import date
from django.utils.timezone import now

Model = M.Model

### Base

@python_2_unicode_compatible
class Base( Model ):
    class Meta:
        abstract = True
    name         = M.SlugField( blank=True )
    title        = M.CharField( max_length=255 )
    description  = M.TextField( blank=True )
    active       = M.BooleanField( default=True )
    valid        = M.BooleanField( default=True )

    def __str__( self ):
        return self.name or self.title


### Metadata

class Note( Base ):
    # relations
    notes   = M.ManyToManyField( 'self', blank=True, related_name='noted' )


class DatePlanMixin( Model ):
    class Meta:
        abstract   = True
    intended_start = M.DateField()
    actual_start   = M.DateField( blank=True )
    intended_end   = M.DateField( blank=True )
    actual_end     = M.DateField( blank=True )
    progress       = M.PositiveSmallIntegerField( default=0 )


class DateTimeMixin( Model ):
    class Meta:
        abstract   = True
    intended_start = M.DateTimeField()
    actual_start   = M.DateTimeField( blank=True )
    intended_end   = M.DateTimeField( blank=True )
    actual_end     = M.DateTimeField( blank=True )


### Input/Output

class Resource( Base ):
    definition  = M.TextField( blank=True )
    url         = M.URLField( max_length=255, blank=True )
    # path        = M.FilePathField()
    upload      = M.FileField( blank=True )
    # relations
    parent      = M.ForeignKey( 'self', M.SET_NULL, null=True, blank=True,
                                related_name='resources' )
    notes       = M.ManyToManyField( Note, blank=True, related_name='resources' )
    attached_to = M.ManyToManyField( Note, blank=True,
                                     related_name='attached_resources' )


class Product( Base ):
    definition  = M.TextField( blank=True )
    url         = M.URLField( max_length=255, blank=True )
    # path        = M.FilePathField()
    upload      = M.FileField( blank=True )
    # relations
    parent      = M.ForeignKey( 'self', M.SET_NULL, null=True, blank=True,
                                related_name='products' )
    notes       = M.ManyToManyField( Note, blank=True, related_name='products' )
    attached_to = M.ManyToManyField( Note, blank=True,
                                     related_name='attached_products' )


class Noted( Base ):
    class Meta:
        abstract = True
    # resources    = M.ManyToManyField( Resource, related_name='%(class)ss' )
    # products     = M.ManyToManyField( Product, related_name='%(class)ss' )
    notes        = M.ManyToManyField( Note, blank=True, related_name='%(class)ss' )


### Strategy

class Goal( Noted, DatePlanMixin ):
    INCOMPLETE = 'icmp'
    FAILURE    = 'fail'
    SUCCESS    = 'succ'
    UPGRADED   = 'upgr'
    OBSOLETED  = 'obst'
    ABANDONED  = 'abnd'
    STATUSES   = (
        ( INCOMPLETE, 'Incomplete' ),
        ( FAILURE,    'Failure'    ),
        ( SUCCESS,    'Success'    ),
        ( UPGRADED,   'Upgraded'   ),
        ( OBSOLETED,  'Obsoleted'  ),
        ( ABANDONED,  'Abandoned'  ),
    )
    status     = M.CharField(
        max_length=4,
        choices=STATUSES,
        default=INCOMPLETE
    )
    # relations
    follows    = M.OneToOneField( 'self', M.SET_NULL, null=True, blank=True,
                                  related_name='precedes' )


class Objective( Noted, DatePlanMixin ):
    status    = M.CharField(
        max_length=4,
        choices=Goal.STATUSES,
        default=Goal.INCOMPLETE
    )
    # relations
    precedes  = M.OneToOneField( 'self', M.SET_NULL, null=True, blank=True,
                                 related_name='follows' )
    goal      = M.ForeignKey( Goal, M.PROTECT, related_name='objectives' )
    satisfies = M.ManyToManyField( Goal, blank=True, related_name='other_objectives' )


class Target( Noted ):
    MET       = 'MET'
    UNMET     = 'UM'
    OBSOLETED = 'OBS'
    BLOCKED   = 'BLK'
    FUTILE    = 'FUT'
    STATUSES  = (
        ( MET,       'Met'       ),
        ( UNMET,     'Unmet'     ),
        ( OBSOLETED, 'Obsoleted' ),
        ( BLOCKED,   'Blocked'   ),
        ( FUTILE,    'Futile'    ),
    )
    progress  = M.PositiveSmallIntegerField( default=0 )
    status    = M.CharField(
        max_length=4,
        choices=STATUSES,
        default=UNMET
    )
    # relations
    objective = M.ForeignKey( Objective, M.CASCADE, related_name='targets' )
    satisfies = M.ManyToManyField( Objective, blank=True,
                                   related_name='other_targets' )
    requires  = M.ManyToManyField( 'self', blank=True, related_name='releases' )


class Strategy( Base ):
    # relations
    objective = M.ForeignKey( Objective, M.PROTECT, related_name='stategies' )
    # resources = M.ManyToManyField( Resource, blank=True, related_name='strategies' )
    # products  = M.ManyToManyField( Product, blank=True, related_name='strategies' )
    notes     = M.ManyToManyField( Note, blank=True, related_name='strategies' )


class Plan( Noted, DatePlanMixin ):
    # relations
    strategy = M.ForeignKey( Strategy, M.PROTECT, related_name='plans' )


class Phase( Noted, DatePlanMixin ):
    # relations
    plan = M.ForeignKey( Plan, M.CASCADE, related_name='phases' )


class Step( Noted, DatePlanMixin ):
    # relations
    phase = M.ForeignKey( Phase, M.CASCADE, related_name='steps' )


### Organization

class Project( Noted, DatePlanMixin ):
    # relations
    objective  = M.ForeignKey( Objective, M.PROTECT, related_name='projects' )
    satisfies  = M.ManyToManyField( Objective, blank=True,
                                    related_name='contributors' )
    strategies = M.ManyToManyField( Strategy, related_name='projects' )
    targets    = M.ManyToManyField( Target, related_name='projects' )
    # TODO: limit_to


class Task( Noted, DatePlanMixin ):
    # relations
    parent  = M.ForeignKey( 'self', M.CASCADE, related_name='subtasks' )
    project = M.ForeignKey( Project, M.CASCADE, blank=True, related_name='tasks' )
    # TODO: maybe default=get_parent_project()
    step    = M.ForeignKey( Step, M.SET_NULL, null=True, blank=True,
                            related_name='tasks' )
    # TODO: limit_to


class Action( Noted, DatePlanMixin ):
    # relations
    follows = M.OneToOneField( 'self', M.SET_NULL, null=True, blank=True,
                               related_name='precedes' )
    task    = M.ForeignKey( Task, M.CASCADE, related_name='actions' )


### Finances

class Currency( Base ):
    rate      = M.FloatField( default=1 )
    # relations
    # resources = M.ManyToManyField( Resource, blank=True, related_name='currencies' )
    notes     = M.ManyToManyField( Note, blank=True, related_name='currencies' )


class Account( Noted ):
    amount   = M.DecimalField( max_digits=16, decimal_places=2, default=0 )
    opened   = M.DateField( default=date.today )
    closed   = M.DateField( blank=True )
    # relations
    currency = M.ForeignKey( Currency, on_delete=M.PROTECT, related_name='accounts' )


class Pool( Noted ):
    size      = M.DecimalField( max_digits=16, decimal_places=2 )
    available = M.DecimalField( max_digits=16, decimal_places=2, default=0 )
    # relations
    parent    = M.ForeignKey( 'self', M.CASCADE, blank=True,
                              related_name='partitions' )
    accounts  = M.ManyToManyField( Account, through='Allotment', blank=True,
                                   related_name='pools' )


class Allotment( Noted ):
    amount  = M.DecimalField( max_digits=16, decimal_places=2 )
    # relations
    account = M.ForeignKey( Account, M.PROTECT, related_name='allotments' )
    pool    = M.ForeignKey( Pool, M.CASCADE, related_name='allotments' )
    # TODO: update pool


class Allocation( Noted ):
    FILLING   = 'fill';
    READY     = 'rdy';
    CLEARED   = 'clr';
    COMMITTED = 'cmt';
    STATUSES  = (
        ( FILLING,   'Filling'   ),
        ( READY,     'Ready'     ),
        ( CLEARED,   'Cleared'   ),
        ( COMMITTED, 'Committed' ),
    )
    opened    = M.DateField()   # TODO: default=now
    used      = M.DateField( blank=True )
    closed    = M.DateField( blank=True )
    size      = M.DecimalField( max_digits=16, decimal_places=2 )
    available = M.DecimalField( max_digits=16, decimal_places=2, default=0 )
    end_state = M.CharField(
        max_length=4,
        choices=STATUSES,
        default=FILLING
    )
    # relations
    pool      = M.ForeignKey( Pool, M.PROTECT, related_name='allocations' )


class Income( Noted, DateTimeMixin ):
    stable = M.BooleanField( default=False )
    amount = M.DecimalField( max_digits=16, decimal_places=2 )
    # relations


class Expense( Noted, DateTimeMixin ):
    stable         = M.BooleanField( default=False )
    amount         = M.DecimalField( max_digits=16, decimal_places=2 )
    # relations
    source         = M.ForeignKey( Allocation, M.PROTECT, related_name='expenses' )


class External( Noted ):
    pass


class Sink( External ):
    external_ptr  = M.OneToOneField( External, M.CASCADE, parent_link=True,
                                     related_name='sink' )
    cost          = M.DecimalField( max_digits=16, decimal_places=2, default=0 )
    expense       = M.ForeignKey( Expense, M.PROTECT, related_name='destinations' )


class Asset( Sink ):
    sink_ptr     = M.OneToOneField( Sink, M.CASCADE, parent_link=True,
                                    related_name='asset' )
    value        = M.DecimalField( max_digits=16, decimal_places=2, default=0 )
    intended_own = M.DateTimeField()
    actual_own   = M.DateTimeField( blank=True )


class Donation( Sink ):
    pass


class Service( Sink ):
    intended  = M.DateTimeField()
    effective = M.DateTimeField( blank=True )


class Rental( Sink, DateTimeMixin ):
    period = M.DurationField()


class Source( External ):
    externalptr = M.OneToOneField( External, M.CASCADE, parent_link=True,
                                   related_name='source' )
    gain            = M.DecimalField( max_digits=16, decimal_places=2, default=0 )
    destination     = M.ForeignKey( Income, M.PROTECT, related_name='sources' )


class Liability( Source ):
    value = M.DecimalField( max_digits=16, decimal_places=2, default=0 )


class Contribution( Source ):
    pass


class Commission( Source ):
    source_ptr      = M.OneToOneField( Source, M.CASCADE, parent_link=True,
                                       related_name='comission' )
    intended_close  = M.DateTimeField()
    effective_close = M.DateTimeField( blank=True )


class Employment( Source, DateTimeMixin ):
    period = M.DurationField()


class Investment( Asset, Commission ):
    pass
    # relations


class Receipt( Noted ):
    amount       = M.DecimalField( max_digits=16, decimal_places=2 )
    intended     = M.DateTimeField()
    effective    = M.DateTimeField( blank=True )
    # relations
    income       = M.ForeignKey( Income, M.PROTECT, related_name='receipts' )
    source       = M.ForeignKey( Source, M.PROTECT, related_name='receipts' )
    destinations = M.ManyToManyField( Account, through='Deposit',
                                      related_name='receipts' )
    # TODO: limit_to


class Deposit( Noted ):
    amount  = M.DecimalField( max_digits=16, decimal_places=2 )
    # relations
    account = M.ForeignKey( Account, M.PROTECT, related_name='deposits' )
    receipt = M.ForeignKey( Receipt, M.CASCADE, related_name='deposits' )


class Payment( Noted ):
    amount      = M.DecimalField( max_digits=16, decimal_places=2 )
    intended    = M.DateTimeField()
    effective   = M.DateTimeField( blank=True )
    # relations
    expense     = M.ForeignKey( Expense, M.PROTECT, related_name='payments' )
    destination = M.ForeignKey( Sink, M.PROTECT, related_name='payments' )


class Budget( Noted ):
    start   = M.DateField()
    end     = M.DateField()
    # relations
    master  = M.ForeignKey( 'self', M.CASCADE, related_name='parts' )
    follows = M.OneToOneField( 'self', M.SET_NULL, null=True, related_name='precedes' )


class Line( Noted ):
    amount    = M.DecimalField( max_digits=16, decimal_places=2 )
    intended  = M.DateTimeField()
    effective = M.DateTimeField( blank=True )
    #relations
    budget    = M.ForeignKey( Budget, M.CASCADE, related_name='lines' )


class Transfer( Line ):
    #relations
    source      = M.ForeignKey( Account, M.CASCADE, related_name='outflow' )
    destination = M.ForeignKey( Account, M.CASCADE, related_name='inflow' )


class Relocation( Line ):
    #relations
    source      = M.ForeignKey( Allocation, M.CASCADE, related_name='outflow' )
    destination = M.ForeignKey( Allocation, M.CASCADE, related_name='inflow' )


class Earning( Line ):
    #relations
    receipt = M.OneToOneField( Receipt, M.CASCADE, related_name='budget_line' )
    # TODO: sync line.intended/effective


class Purchase( Line ):
    #relations
    payment = M.OneToOneField( Payment, M.CASCADE, related_name='budget_line' )
    # TODO: sync line.intended/effective


### Teamwork

class Team( Noted ):
    # relations
    parent  = M.ForeignKey( 'self', M.CASCADE, related_name='groups' )


class Position( Noted ):
    # relations
    team = M.ForeignKey( Team, M.CASCADE, related_name='positions' )


class Role( Noted ):
    # relations
    positions = M.ManyToManyField( Position, blank=True, related_name='roles' )


class Responsibility( Base ):
    # relations
    roles     = M.ManyToManyField( Role, blank=True, related_name='responsibilities' )
    # resources = M.ManyToManyField( Resource, related_name='responsibilities' )
    # products  = M.ManyToManyField( Product, related_name='responsibilities' )
    notes     = M.ManyToManyField( Product, blank=True,
                                   related_name='responsibilities' )


class Capacity( Base ):
    # relations
    roles     = M.ManyToManyField( Role, blank=True, related_name='capacities' )
    # resources = M.ManyToManyField( Resource, related_name='capacities' )
    # products  = M.ManyToManyField( Product, related_name='capacities' )
    notes     = M.ManyToManyField( Note, blank=True, related_name='capacities' )


class User( Noted ):
    # @property
    # def teams()
    # TODO: this
    positions = M.ManyToManyField( Position, blank=True, related_name='users' )
    # TODO: add user to team => get default team position

    def __str__( self ):
        return self.name or self.title


### Taxonomy

class Taxonomy( Base ):
    hierarhichal = M.BooleanField()
    exclusive    = M.BooleanField()
    # relations
    parent       = M.ForeignKey( 'self', M.CASCADE, related_name='children' )
    # resources    = M.ManyToManyField( Resource, related_name='taxonomies' )
    # products     = M.ManyToManyField( Product, related_name='taxonomies' )
    notes        = M.ManyToManyField( Note, blank=True, related_name='taxonomies' )


class Term( Noted ):
    # relations
    parent = M.ForeignKey( 'self', M.CASCADE, related_name='children' )
    data   = JSONField( default=dict )

