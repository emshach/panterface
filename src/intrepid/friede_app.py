# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, include
from rest_framework import routers
from collections import OrderedDict
from friede.core import installapp
from . import views


app_name = 'intrepid'

objects = '''note resource product goal objective target strategy plan phase
        step project task action currency account pool allotment allocation
        income expense asset donation service rental liability contribution
        commission employment investment receipt deposit payment budget line
        transfer relocation earning purchase team position role responsibility
        capacity user taxonomy term'''.split()
relations = dict(
    note={
        'model'  : 'Note',
        'plural' : 'notes',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    resource={
        'model'  : 'Resource',
        'plural' : 'resources',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    product={
        'model'  : 'Product',
        'plural' : 'products',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    goal={
        'model'  : 'Goal',
        'plural' : 'goals',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    objective={
        'model'  : 'Objective',
        'plural' : 'objectives',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    target={
        'model'  : 'Target',
        'plural' : 'targets',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    strategy={
        'model'  : 'Strategy',
        'plural' : 'strategies',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    plan={
        'model'  : 'Plan',
        'plural' : 'plans',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    phase={
        'model'  : 'Phase',
        'plural' : 'phases',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    step={
        'model'  : 'Step',
        'plural' : 'steps',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    project={
        'model'  : 'Project',
        'plural' : 'projects',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    task={
        'model'  : 'Task',
        'plural' : 'tasks',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    action={
        'model'  : 'Action',
        'plural' : 'actions',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    currency={
        'model'  : 'Currency',
        'plural' : 'currencies',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    account={
        'model'  : 'Account',
        'plural' : 'accounts',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    pool={
        'model'  : 'Pool',
        'plural' : 'pools',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    allotment={
        'model'  : 'Allotment',
        'plural' : 'allotments',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    allocation={
        'model'  : 'Allocation',
        'plural' : 'allocations',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    income={
        'model'  : 'Income',
        'plural' : 'incomes',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    expense={
        'model'  : 'Expense',
        'plural' : 'expenses',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    asset={
        'model'  : 'Asset',
        'plural' : 'assets',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    donation={
        'model'  : 'Donation',
        'plural' : 'donations',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    service={
        'model'  : 'Service',
        'plural' : 'services',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    rental={
        'model'  : 'Rental',
        'plural' : 'rentals',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    liability={
        'model'  : 'Liability',
        'plural' : 'liabilities',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    contribution={
        'model'  : 'Contribution',
        'plural' : 'contributions',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    commission={
        'model'  : 'Commission',
        'plural' : 'commissions',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    employment={
        'model'  : 'Employment',
        'plural' : 'employments',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    investment={
        'model'  : 'Investment',
        'plural' : 'investments',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    receipt={
        'model'  : 'Receipt',
        'plural' : 'receipts',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    deposit={
        'model'  : 'Deposit',
        'plural' : 'deposits',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    payment={
        'model'  : 'Payment',
        'plural' : 'payments',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    budget={
        'model'  : 'Budget',
        'plural' : 'budgets',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    line={
        'model'  : 'Line',
        'plural' : 'lines',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    transfer={
        'model'  : 'Transfer',
        'plural' : 'transfers',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    relocation={
        'model'  : 'Relocation',
        'plural' : 'relocations',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    earning={
        'model'  : 'Earning',
        'plural' : 'earnings',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    purchase={
        'model'  : 'Purchase',
        'plural' : 'purchases',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    team={
        'model'  : 'Team',
        'plural' : 'teams',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    position={
        'model'  : 'Position',
        'plural' : 'positions',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    role={
        'model'  : 'Role',
        'plural' : 'roles',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    responsibility={
        'model'  : 'Responsibility',
        'plural' : 'responsibilities',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    capacity={
        'model'  : 'Capacity',
        'plural' : 'capacities',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    user={
        'model'  : 'User',
        'plural' : 'users',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    taxonomy={
        'model'  : 'Taxonomy',
        'plural' : 'taxonomies',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
    term={
        'model'  : 'Term',
        'plural' : 'terms',
        'has'    : ''.split(),
        'in'     : ''.split()
    },
)
actions = 'list view new edit report delete'.split()
def install():
    app, new = installapp(
        name='intrepid',
        module='intrepid',
        title='Project Intrepid',
        description='''Time, task and finance management system

Also includes goal-setting, strategizing, and teamwork tools.''',
        data=(
            ( '0.1.0',
              ( 'locations', ( 'from relations', objects, relations )),
              ( 'settings', ( 'from relations', objects, relations )),
              ( 'links', ),
              ( 'widgets',
                tuple(
                    ( action,
                      tuple(( o, dict(
                          extends="widgets.{}.from.model".format( action ),
                          data=dict(
                              model="intrepid.{}".format( relations[o][ 'model' ]))
                      )) for o in objects ))
                    for action in actions[1:] )),
              ( 'blocks',
                ( 'form',
                  ( 'basic', dict(
                      extends='blocks.form.section',
                      data=dict( fields='active name title description'.split() ))),
                  ( 'extra',
                    ( 'resources', dict(
                        extends='blocks.form.section',
                        data=dict( fields='url upload parent attached_to'.split() ))),
                    ( 'goal', dict(
                        extends='blocks.form.section'
                    )),
                    # ( 'objective', ),
                    # ( 'target', ),
                    # ( 'strategy', ),
                    # ( 'plan', ),
                    # ( 'phase', ),
                    # ( 'step', ),
                    # ( 'project', ),
                    # ( 'task', ),
                    # ( 'action', ),
                    # ( 'currency', ),
                    # ( 'account', ),
                    # ( 'pool', ),
                    # ( 'allotment', ),
                    # ( 'allocation', ),
                    # ( 'income', ),
                    # ( 'expense', ),
                    # ( 'asset', ),
                    # ( 'donation', ),
                    # ( 'service', ),
                    # ( 'rental', ),
                    # ( 'liability', ),
                    # ( 'contribution', ),
                    # ( 'commission', ),
                    # ( 'employment', ),
                    # ( 'investment', ),
                    # ( 'receipt', ),
                    # ( 'deposit', ),
                    # ( 'payment', ),
                    # ( 'budget', ),
                    # ( 'line', ),
                    # ( 'transfer', ),
                    # ( 'relocation', ),
                    # ( 'earning', ),
                    # ( 'purchase', ),
                    # ( 'team', ),
                    # ( 'position', ),
                    # ( 'role', ),
                    # ( 'responsibility', ),
                    # ( 'capacity', ),
                    # ( 'user', ),
                    # ( 'taxonomy', ),
                    # ( 'term', ),
                )
                  ( 'relations',
                    ( 'note', dict(
                        extends='blocks.form.section',
                        data=dict( fields='notes'.split() ))),
                    ( 'resource', dict(
                        extends='blocks.form.section',
                        data=dict( fields='resources notes'.split() ))),
                    ( 'product', dict(
                        extends='blocks.form.section',
                        data=dict( fields='products notes'.split() ))),
                    ( 'goal', dict(
                        extends='blocks.form.section',
                        data=dict( fields='''intended_start intended_end actual_start
                                         actual_end'''.split() )
                    )),
                    # ( 'objective', ),
                    # ( 'target', ),
                    # ( 'strategy', ),
                    # ( 'plan', ),
                    # ( 'phase', ),
                    # ( 'step', ),
                    # ( 'project', ),
                    # ( 'task', ),
                    # ( 'action', ),
                    # ( 'currency', ),
                    # ( 'account', ),
                    # ( 'pool', ),
                    # ( 'allotment', ),
                    # ( 'allocation', ),
                    # ( 'income', ),
                    # ( 'expense', ),
                    # ( 'asset', ),
                    # ( 'donation', ),
                    # ( 'service', ),
                    # ( 'rental', ),
                    # ( 'liability', ),
                    # ( 'contribution', ),
                    # ( 'commission', ),
                    # ( 'employment', ),
                    # ( 'investment', ),
                    # ( 'receipt', ),
                    # ( 'deposit', ),
                    # ( 'payment', ),
                    # ( 'budget', ),
                    # ( 'line', ),
                    # ( 'transfer', ),
                    # ( 'relocation', ),
                    # ( 'earning', ),
                    # ( 'purchase', ),
                    # ( 'team', ),
                    # ( 'position', ),
                    # ( 'role', ),
                    # ( 'responsibility', ),
                    # ( 'capacity', ),
                    # ( 'user', ),
                    # ( 'taxonomy', ),
                    # ( 'term', ),
              ),
                  ( 'infographic', dict(
                      extends='blocks.form.calendar',
                      data=dict(
                          dates=[
                              dict( model='intrepid.Goal',
                                    start='intended_start',
                                    end='intended_end' ),
                              dict( model='intrepid.Goal',
                                    start='actual_start',
                                    end='actual_end' )]))))),
              ( 'screens',
                ( 'list',
                  tuple(
                      ( o, dict(
                          extends='screens.list.from.model',
                          model=relations[o][ 'model' ]))
                    for o in objects)),
                ( 'new',
                  ( 'note', dict(
                      extends='screens.form.single',
                      block_entries=
                      ( 'slot',
                        dict( block='form.basic' ),
                        dict( block='form.relations.note' ))
                  )),
                  ( 'resource', dict(
                      extends='screens.form.single',
                      block_entries=
                      ( 'slot',
                        dict( block='form.basic' ),
                        dict( block='form.extra.resource' ),
                        dict( block='form.relations.resource' )))),
                  ( 'product', dict(
                      extends='screens.form.single',
                      block_entries=
                      ( 'slot',
                        dict( block='form.basic' ),
                        dict( block='form.extra.product' ),
                        dict( block='form.relations.product' )))),
                  ( 'goal', dict(
                      extends='screens.form.single',
                      block_entries=
                      ( 'slot',
                        dict( block='form.basic' ),
                        dict( block='form.infobox.goal' ),
                        dict( block='form.extra.goal' ),
                        dict( block='form.relations.goal' )))),
                  # ( 'objective', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.objective' ),
                  #       dict( block='form.relations.objective' )))),
                  # ( 'target', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.target' ),
                  #       dict( block='form.relations.target' )))),
                  # ( 'strategy', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.strategy' ),
                  #       dict( block='form.relations.strategy' )))),
                  # ( 'plan', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.plan' ),
                  #       dict( block='form.relations.plan' )))),
                  # ( 'phase', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.phase' ),
                  #       dict( block='form.relations.phase' )))),
                  # ( 'step', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.step' ),
                  #       dict( block='form.relations.step' )))),
                  # ( 'project', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.project' ),
                  #       dict( block='form.relations.project' )))),
                  # ( 'task', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.task' ),
                  #       dict( block='form.relations.task' )))),
                  # ( 'action', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.action' ),
                  #       dict( block='form.relations.action' )))),
                  # ( 'currency', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.currency' ),
                  #       dict( block='form.relations.currency' )))),
                  # ( 'account', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.account' ),
                  #       dict( block='form.relations.account' )))),
                  # ( 'pool', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.pool' ),
                  #       dict( block='form.relations.pool' )))),
                  # ( 'allotment', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.allotment' ),
                  #       dict( block='form.relations.allotment' )))),
                  # ( 'allocation', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.allocation' ),
                  #       dict( block='form.relations.allocation' )))),
                  # ( 'income', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.income' ),
                  #       dict( block='form.relations.income' )))),
                  # ( 'expense', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.expense' ),
                  #       dict( block='form.relations.expense' )))),
                  # ( 'asset', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.asset' ),
                  #       dict( block='form.relations.asset' )))),
                  # ( 'donation', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.donation' ),
                  #       dict( block='form.relations.donation' )))),
                  # ( 'service', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.service' ),
                  #       dict( block='form.relations.service' )))),
                  # ( 'rental', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.rental' ),
                  #       dict( block='form.relations.rental' )))),
                  # ( 'liability', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.liability' ),
                  #       dict( block='form.relations.liability' )))),
                  # ( 'contribution', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.contribution' ),
                  #       dict( block='form.relations.contribution' )))),
                  # ( 'commission', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.commission' ),
                  #       dict( block='form.relations.commission' )))),
                  # ( 'employment', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.employment' ),
                  #       dict( block='form.relations.employment' )))),
                  # ( 'investment', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.investment' ),
                  #       dict( block='form.relations.investment' )))),
                  # ( 'receipt', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.receipt' ),
                  #       dict( block='form.relations.receipt' )))),
                  # ( 'deposit', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.deposit' ),
                  #       dict( block='form.relations.deposit' )))),
                  # ( 'payment', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.payment' ),
                  #       dict( block='form.relations.payment' )))),
                  # ( 'budget', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.budget' ),
                  #       dict( block='form.relations.budget' )))),
                  # ( 'line', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.line' ),
                  #       dict( block='form.relations.line' )))),
                  # ( 'transfer', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.transfer' ),
                  #       dict( block='form.relations.transfer' )))),
                  # ( 'relocation', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.relocation' ),
                  #       dict( block='form.relations.relocation' )))),
                  # ( 'earning', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.earning' ),
                  #       dict( block='form.relations.earning' )))),
                  # ( 'purchase', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.purchase' ),
                  #       dict( block='form.relations.purchase' )))),
                  # ( 'team', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.team' ),
                  #       dict( block='form.relations.team' )))),
                  # ( 'position', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.position' ),
                  #       dict( block='form.relations.position' )))),
                  # ( 'role', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.role' ),
                  #       dict( block='form.relations.role' )))),
                  # ( 'responsibility', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.responsibility' ),
                  #       dict( block='form.relations.responsibility' )))),
                  # ( 'capacity', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.capacity' ),
                  #       dict( block='form.relations.capacity' )))),
                  # ( 'user', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.user' ),
                  #       dict( block='form.relations.user' )))),
                  # ( 'taxonomy', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.taxonomy' ),
                  #       dict( block='form.relations.taxonomy' )))),
                  # ( 'term', dict(
                  #     extends='form.single',
                  #     block_entries=
                  #     ( 'slot',
                  #       dict( block='form.basic' ),
                  #       dict( block='form.extra.term' ),
                  #       dict( block='form.relations.term' )))),
                ),
              ),
              # ( '', ),
            ),
        ))

def init( router, register, urlpatterns ):
    register( r'notes',            views.NoteViewSet           )
    register( r'resources',        views.ResourceViewSet       )
    register( r'products',         views.ProductViewSet        )
    register( r'goals',            views.GoalViewSet           )
    register( r'objectives',       views.ObjectiveViewSet      )
    register( r'targets',          views.TargetViewSet         )
    register( r'strategies',       views.StrategyViewSet       )
    register( r'plans',            views.PlanViewSet           )
    register( r'phases',           views.PhaseViewSet          )
    register( r'steps',            views.StepViewSet           )
    register( r'projects',         views.ProjectViewSet        )
    register( r'tasks',            views.TaskViewSet           )
    register( r'actions',          views.ActionViewSet         )
    register( r'currencies',       views.CurrencyViewSet       )
    register( r'accounts',         views.AccountViewSet        )
    register( r'pools',            views.PoolViewSet           )
    register( r'allotments',       views.AllotmentViewSet      )
    register( r'allocations',      views.AllocationViewSet     )
    register( r'incomes',          views.IncomeViewSet         )
    register( r'expenses',         views.ExpenseViewSet        )
    register( r'assets',           views.AssetViewSet          )
    register( r'donations',        views.DonationViewSet       )
    register( r'services',         views.ServiceViewSet        )
    register( r'rentals',          views.RentalViewSet         )
    register( r'liabilities',      views.LiabilityViewSet      )
    register( r'contributions',    views.ContributionViewSet   )
    register( r'commissions',      views.CommissionViewSet     )
    register( r'employments',      views.EmploymentViewSet     )
    register( r'investments',      views.InvestmentViewSet     )
    register( r'receipts',         views.ReceiptViewSet        )
    register( r'deposits',         views.DepositViewSet        )
    register( r'payments',         views.PaymentViewSet        )
    register( r'budgets',          views.BudgetViewSet         )
    register( r'lines',            views.LineViewSet           )
    register( r'transfers',        views.TransferViewSet       )
    register( r'relocations',      views.RelocationViewSet     )
    register( r'earnings',         views.EarningViewSet        )
    register( r'purchases',        views.PurchaseViewSet       )
    register( r'teams',            views.TeamViewSet           )
    register( r'positions',        views.PositionViewSet       )
    register( r'roles',            views.RoleViewSet           )
    register( r'responsibilities', views.ResponsibilityViewSet )
    register( r'capacities',       views.CapacityViewSet       )
    register( r'users',            views.UserViewSet           )
    register( r'taxonomies',       views.TaxonomyViewSet       )
    register( r'terms',            views.TermViewSet           )
