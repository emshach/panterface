# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.utils.encoding import python_2_unicode_compatible
from django.db import models as M
from django.contrib.postgres.fields import JSONField
from datetime import date
from django.utils.timezone import now
from aries.models import OwnedModel, Role as authRole, Group, Permission
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

Model = M.Model

### Base

@python_2_unicode_compatible
class Base( OwnedModel ):
    class Meta:
        abstract = True
    name         = M.SlugField( null=True, blank=True )
    title        = M.CharField( max_length=255 )
    description  = M.TextField( null=True,blank=True )
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
    intended_start = M.DateField( null=True, blank=True )
    actual_start   = M.DateField( null=True, blank=True )
    intended_end   = M.DateField( null=True, blank=True )
    actual_end     = M.DateField( null=True, blank=True )
    progress       = M.PositiveSmallIntegerField( default=0 )


class DateTimeMixin( Model ):
    class Meta:
        abstract   = True
    intended_start = M.DateTimeField( null=True, blank=True )
    actual_start   = M.DateTimeField( null=True, blank=True )
    intended_end   = M.DateTimeField( null=True, blank=True )
    actual_end     = M.DateTimeField( null=True, blank=True )


### Input/Output

class Resource( Base ):
    definition  = M.TextField( null=True, blank=True )
    uri         = M.CharField( max_length=255, null=True, blank=True )
    # path        = M.FilePathField()
    upload      = M.FileField( null=True, blank=True )
    # relations
    parent      = M.ForeignKey( 'self', M.SET_NULL, null=True, blank=True,
                                related_name='resources' )
    notes       = M.ManyToManyField( Note, blank=True, related_name='resources' )
    attached_to = M.ManyToManyField( Note, blank=True, related_name='attached_resources' )


class Product( Base ):
    definition  = M.TextField( null=True, blank=True )
    uri         = M.CharField( max_length=255, null=True, blank=True )
    # path        = M.FilePathField()
    upload      = M.FileField( null=True, blank=True )
    # relations
    parent      = M.ForeignKey( 'self', M.SET_NULL, null=True, blank=True,
                                related_name='products' )
    notes       = M.ManyToManyField( Note, blank=True, related_name='products' )
    attached_to = M.ManyToManyField( Note, blank=True,
                                     related_name='attached_products' )


class Noted( Base ):
    class Meta:
        abstract = True
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


class Strategy( Noted ):
    class Meta:
        verbose_name_plural = 'strategies'
    # relations
    objective  = M.ForeignKey( Objective, M.PROTECT, related_name='stategies' )
    notes      = M.ManyToManyField( Note, blank=True, related_name='strategies' )
    targets    = M.ManyToManyField( Target, blank=True, related_name='strategies' )


class Plan( Noted, DatePlanMixin ):
    # relations
    strategy = M.ForeignKey( Strategy, M.PROTECT, related_name='plans' )
    targets  = M.ManyToManyField( Target, blank=True, related_name='plans' )


class Phase( Noted, DatePlanMixin ):
    # relations
    plan    = M.ForeignKey( Plan, M.CASCADE, related_name='phases' )
    targets = M.ManyToManyField( Target, blank=True, related_name='phases' )


class Step( Noted, DatePlanMixin ):
    # relations
    phase   = M.ForeignKey( Phase, M.CASCADE, related_name='steps' )
    targets = M.ManyToManyField( Target, blank=True, related_name='steps' )


### Organization

class Project( Noted, DatePlanMixin ):
    # relations
    objective  = M.ForeignKey( Objective, M.PROTECT, related_name='projects' )
    satisfies  = M.ManyToManyField( Objective, blank=True,
                                    related_name='contributors' )
    strategies = M.ManyToManyField( Strategy, blank=True, related_name='projects' )
    targets    = M.ManyToManyField( Target, blank=True, related_name='projects' )
    # TODO: limit_to


class Task( Noted, DatePlanMixin ):
    # relations
    parent  = M.ForeignKey( 'self', M.CASCADE, related_name='subtasks' )
    project = M.ForeignKey( Project, M.CASCADE, null=True, blank=True,
                            related_name='tasks' )
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

class Currency( Noted ):
    class Meta:
        verbose_name_plural = 'currencies'
    rate      = M.FloatField( default=1 )
    # relations
    notes     = M.ManyToManyField( Note, blank=True, related_name='currencies' )


class Account( Noted ):
    amount   = M.DecimalField( max_digits=16, decimal_places=2, default=0 )
    opened   = M.DateField( default=date.today, null=True, blank=True )
    closed   = M.DateField( null=True, blank=True )
    # relations
    currency = M.ForeignKey( Currency, on_delete=M.PROTECT, related_name='accounts' )


class Pool( Noted ):
    size      = M.DecimalField( max_digits=16, decimal_places=2, default=0 )
    available = M.DecimalField( max_digits=16, decimal_places=2, default=0 )
    # relations
    parent    = M.ForeignKey( 'self', M.CASCADE, null=True, blank=True,
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
    opened    = M.DateField( default=date.today )
    used      = M.DateField( null=True, blank=True )
    closed    = M.DateField( null=True, blank=True )
    size      = M.DecimalField( max_digits=16, decimal_places=2, default=0 )
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
    amount = M.DecimalField( max_digits=16, decimal_places=2, default=0 )
    # relations


class Expense( Noted, DateTimeMixin ):
    stable         = M.BooleanField( default=False )
    amount         = M.DecimalField( max_digits=16, decimal_places=2, default=0 )
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
    sink_ptr      = M.OneToOneField( Sink, M.CASCADE, parent_link=True,
                                    related_name='asset' )
    value         = M.DecimalField( max_digits=16, decimal_places=2, default=0 )
    intended_own  = M.DateTimeField( null=True, blank=True )
    effective_own = M.DateTimeField( null=True, blank=True )


class Donation( Sink ):
    pass


class Service( Sink ):
    intended  = M.DateTimeField( null=True, blank=True )
    effective = M.DateTimeField( null=True, blank=True )


class Rental( Sink, DateTimeMixin ):
    period = M.DurationField( null=True, blank=True )


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
    intended_close  = M.DateTimeField( null=True, blank=True )
    effective_close = M.DateTimeField( null=True, blank=True )


class Employment( Source, DateTimeMixin ):
    period = M.DurationField( null=True, blank=True )


class Investment( Asset, Commission ):
    pass
    # relations


class Receipt( Noted ):
    amount       = M.DecimalField( max_digits=16, decimal_places=2 )
    intended     = M.DateTimeField( null=True, blank=True )
    effective    = M.DateTimeField( null=True, blank=True )
    # relations
    income       = M.ForeignKey( Income, M.PROTECT, related_name='receipts' )
    source       = M.ForeignKey( Source, M.PROTECT, related_name='receipts' )
    destinations = M.ManyToManyField( Account, through='Deposit',
                                      related_name='receipts' )
    # TODO: limit_to


class Deposit( Noted ):
    amount  = M.DecimalField( max_digits=16, decimal_places=2, default=0 )
    # relations
    account = M.ForeignKey( Account, M.PROTECT, related_name='deposits' )
    receipt = M.ForeignKey( Receipt, M.CASCADE, related_name='deposits' )


class Payment( Noted ):
    amount      = M.DecimalField( max_digits=16, decimal_places=2, default=0 )
    intended    = M.DateTimeField( null=True, blank=True )
    effective   = M.DateTimeField( null=True, blank=True )
    # relations
    expense     = M.ForeignKey( Expense, M.PROTECT, related_name='payments' )
    destination = M.ForeignKey( Sink, M.PROTECT, related_name='payments' )


class Budget( Noted ):
    start   = M.DateField( null=True, blank=True )
    end     = M.DateField( null=True, blank=True )
    # relations
    master  = M.ForeignKey( 'self', M.CASCADE, related_name='parts' )
    follows = M.OneToOneField( 'self', M.SET_NULL, null=True, blank=True,
                               related_name='precedes' )


class Line( Noted ):
    amount    = M.DecimalField( max_digits=16, decimal_places=2, default=0 )
    intended  = M.DateTimeField( null=True, blank=True )
    effective = M.DateTimeField( null=True, blank=True )
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
    parent     = M.ForeignKey( 'self', M.CASCADE, related_name='groups' )
    members    = M.ManyToManyField( get_user_model(), through='Position',
                                    related_name='intrepid_teams' )
    auth_group = GenericRelation( Group,
                                  related_query_name="%(app_label)s_%(class)s",
                                  content_type_field='manager_type',
                                  object_id_field='manager_id' )



class Position( Noted ):
    # relations
    team = M.ForeignKey( Team, M.CASCADE, related_name='positions' )
    member = M.ForeignKey( get_user_model(), null=True, blank=True,
                           related_name='intrepid_positions' )


class Role( Noted ):
    # relations
    positions = M.ManyToManyField( Position, blank=True, related_name='roles' )
    system = M.ManyToManyField( authRole, blank=True, related_name='intrepid_roles' )


class Responsibility( Noted ):
    class Meta:
        verbose_name_plural = 'responsibilities'
    # relations
    roles     = M.ManyToManyField( Role, blank=True, related_name='responsibilities' )
    notes     = M.ManyToManyField( Product, blank=True,
                                   related_name='responsibilities' )


class Capacity( Noted ):
    class Meta:
        verbose_name_plural = 'capacities'
    # relations
    roles       = M.ManyToManyField( Role, blank=True, related_name='capacities' )
    permissions = M.ManyToManyField( Permission, blank=True,
                                     related_name='intrepid_capacities' )
    notes       = M.ManyToManyField( Note, blank=True, related_name='capacities' )

### Taxonomy

class Taxonomy( Noted ):
    class Meta:
        verbose_name_plural = 'taxonomies'
    hierarchichal = M.BooleanField( default=False )
    exclusive     = M.BooleanField( default=True )
    # relations
    parent        = M.ForeignKey( 'self', M.CASCADE, null=True, blank=True,
                                  related_name='children' )
    notes         = M.ManyToManyField( Note, blank=True, related_name='taxonomies' )


class Term( Noted ):
    data   = JSONField( default=dict )
    # relations
    parent = M.ForeignKey( 'self', M.CASCADE, null=True, blank=True,
                           related_name='children' )
    taxonomy = M.ForeignKey( Taxonomy, M.CASCADE, related_name='terms' )

