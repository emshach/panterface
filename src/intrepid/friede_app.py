# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import views
from friede import app

class App( app.App ):
    name        =  'intrepid'
    icon        = 'fontawesome.gem'
    module      = 'intrepid'
    title       = 'Project Intrepid',
    description = '''Time, task and finance management system

    Also includes goal-setting, strategizing, and teamwork tools.'''

    objects = '''note resource product goal objective target strategy plan phase
            step project task action currency account pool allotment allocation
            income expense asset donation service rental liability contribution
            commission employment investment receipt deposit payment budget transfer
            relocation earning purchase team position role responsibility capacity
            user taxonomy term'''.split()
    relations = dict(
        note={
            'model'  : 'Note',
            'icon'   : 'fontawesome.sticky-note',
            'plural' : 'notes',
            'has'    : 'note resource product'.split(),
            'in'     : objects
        },
        resource={
            'model'  : 'Resource',
            'icon'   : 'fontawesome.sign-in-alt',
            'plural' : 'resources',
            'has'    : 'note resource'.split(),
            'in'     : 'note resource'.split()
        },
        product={
            'model'  : 'Product',
            'icon'   : 'fontawesome.sign-out-alt',
            'plural' : 'products',
            'has'    : 'note product'.split(),
            'in'     : 'note product'.split()
        },
        goal={
            'model'  : 'Goal',
            'icon'   : 'fontawesome.trophy',
            'plural' : 'goals',
            'has'    : 'note objective'.split(),
            'in'     : 'objective'.split()
        },
        objective={
            'model'  : 'Objective',
            'icon'   : 'fontawesome.bullseye',
            'plural' : 'objectives',
            'has'    : 'note target strategy project goal'.split(),
            'in'     : 'goal target project'.split()
        },
        target={
            'model'  : 'Target',
            'icon'   : 'fontawesome.crosshairs',
            'plural' : 'targets',
            'has'    : 'note objective'.split(),
            'in'     : 'objective strategy plan phase step project'.split()
        },
        strategy={
            'model'  : 'Strategy',
            'icon'   : 'fontawesome.chess-knight',
            'plural' : 'strategies',
            'has'    : 'note plan target'.split(),
            'in'     : 'objective project'.split()
        },
        plan={
            'model'  : 'Plan',
            'icon'   : 'fontawesome.sitemap',
            'plural' : 'plans',
            'has'    : 'note phase target'.split(),
            'in'     : 'strategy'.split()
        },
        phase={
            'model'  : 'Phase',
            'icon'   : 'fontawesome.bookmark',
            'plural' : 'phases',
            'has'    : 'note step target'.split(),
            'in'     : 'plan'.split()
        },
        step={
            'model'  : 'Step',
            'icon'   : 'fontawesome.shoe-prints',
            'plural' : 'steps',
            'has'    : 'note task target'.split(),
            'in'     : 'phase'.split()
        },
        project={
            'model'  : 'Project',
            'icon'   : 'fontawesome.project-diagram',
            'plural' : 'projects',
            'has'    : 'note task objective strategy target'.split(),
            'in'     : 'objective'.split()
        },
        task={
            'model'  : 'Task',
            'icon'   : 'fontawesome.tasks',
            'plural' : 'tasks',
            'has'    : 'note action task'.split(),
            'in'     : 'project task step'.split()
        },
        action={
            'model'  : 'Action',
            'icon'   : 'fontawesome.walking',
            'plural' : 'actions',
            'has'    : 'note'.split(),
            'in'     : 'task'.split()
        },
        currency={
            'model'  : 'Currency',
            'icon'   : 'fontawesome.money-bill-wave',
            'plural' : 'currencies',
            'has'    : 'note'.split(),
            'in'     : ''.split()
        },
        account={
            'model'  : 'Account',
            'icon'   : 'fontawesome.piggy-bank',
            'plural' : 'accounts',
            'has'    : 'note receipt deposit'.split(),
            'in'     : 'pool receipt'.split()
        },
        pool={
            'model'  : 'Pool',
            'icon'   : 'fontawesome.coins',
            'plural' : 'pools',
            'has'    : 'note pool account allotment allocation'.split(),
            'in'     : 'pool'.split()
        },
        allotment={
            'model'  : 'Allotment',
            'icon'   : 'fontawesome.money-check-alt',
            'plural' : 'allotments',
            'has'    : 'note'.split(),
            'in'     : 'pool'.split()
        },
        allocation={
            'model'  : 'Allocation',
            'icon'   : 'fontawesome.wallet',
            'plural' : 'allocations',
            'has'    : 'note'.split(),
            'in'     : 'pool expense'.split()
        },
        income={
            'model'  : 'Income',
            'icon'   : 'fontawesome.hand-holding-usd',
            'plural' : 'incomes',
            'has'    : '''note liability contribution commission employment investment
                          receipt'''.split(),
            'in'     : ''.split()
        },
        expense={
            'model'  : 'Expense',
            'icon'   : 'fontawesome.credit-card',
            'plural' : 'expenses',
            'has'    : 'note asset donation service rental investment payment'.split(),
            'in'     : 'allocation'.split()
        },
        asset={
            'model'  : 'Asset',
            'icon'   : 'fontawesome.home',
            'plural' : 'assets',
            'has'    : 'note payment'.split(),
            'in'     : 'expense'.split()
        },
        donation={
            'model'  : 'Donation',
            'icon'   : 'fontawesome.donate',
            'plural' : 'donations',
            'has'    : 'note payment'.split(),
            'in'     : 'expense'.split()
        },
        service={
            'model'  : 'Service',
            'icon'   : 'fontawesome.taxi',
            'plural' : 'services',
            'has'    : 'note payment'.split(),
            'in'     : 'expense'.split()
        },
        rental={
            'model'  : 'Rental',
            'icon'   : 'fontawesome.truck-moving',
            'plural' : 'rentals',
            'has'    : 'note payment'.split(),
            'in'     : 'expense'.split()
        },
        liability={
            'model'  : 'Liability',
            'icon'   : 'fontawesome.file-contract',
            'plural' : 'liabilities',
            'has'    : 'note'.split(),
            'in'     : 'income'.split()
        },
        contribution={
            'model'  : 'Contribution',
            'icon'   : 'fontawesome.money-check',
            'plural' : 'contributions',
            'has'    : 'note'.split(),
            'in'     : 'income'.split()
        },
        commission={
            'model'  : 'Commission',
            'icon'   : 'fontawesome.drafting-compass',
            'plural' : 'commissions',
            'has'    : 'note'.split(),
            'in'     : 'income'.split()
        },
        employment={
            'model'  : 'Employment',
            'icon'   : 'fontawesome.user-md',
            'plural' : 'employments',
            'has'    : 'note'.split(),
            'in'     : 'income'.split()
        },
        investment={
            'model'  : 'Investment',
            'icon'   : 'fontawesome.warehouse',
            'plural' : 'investments',
            'has'    : 'note'.split(),
            'in'     : 'income expense'.split()
        },
        receipt={
            'model'  : 'Receipt',
            'icon'   : 'fontawesome.receipt',
            'plural' : 'receipts',
            'has'    : 'note account'.split(),
            'in'     : '''income liability contribution commission employment investment
                          account deposit earning'''.split()
        },
        deposit={
            'model'  : 'Deposit',
            'icon'   : 'fontawesome.download',
            'plural' : 'deposits',
            'has'    : 'note receipt account'.split(),
            'in'     : ''.split()
        },
        payment={
            'model'  : 'Payment',
            'icon'   : 'fontawesome.cart-arrow-down',
            'plural' : 'payments',
            'has'    : 'note'.split(),
            'in'     : 'expense asset donation service rental purchase'.split()
        },
        budget={
            'model'  : 'Budget',
            'icon'   : 'fontawesome.chart-line',
            'plural' : 'budgets',
            'has'    : 'note budget'.split(),
            'in'     : 'budget transfer relocation earning purchase'.split()
        },
        transfer={
            'model'  : 'Transfer',
            'icon'   : 'fontawesome.exchange-alt',
            'plural' : 'transfers',
            'has'    : 'note'.split(),
            'in'     : 'liability contribution commission employment'.split()
        },
        relocation={
            'model'  : 'Relocation',
            'icon'   : 'fontawesome.sync-alt',
            'plural' : 'relocations',
            'has'    : 'note'.split(),
            'in'     : 'allocation'.split()
        },
        earning={
            'model'  : 'Earning',
            'icon'   : 'fontawesome.dollar-sign',
            'plural' : 'earnings',
            'has'    : 'note receipt'.split(),
            'in'     : ''.split()
        },
        purchase={
            'model'  : 'Purchase',
            'icon'   : 'fontawesome.store-alt',
            'plural' : 'purchases',
            'has'    : 'note payment'.split(),
            'in'     : ''.split()
        },
        team={
            'model'  : 'Team',
            'icon'   : 'fontawesome.users',
            'plural' : 'teams',
            'has'    : 'note team'.split(),
            'in'     : 'team position'.split()
        },
        position={
            'model'  : 'Position',
            'icon'   : 'fontawesome.user-graduate',
            'plural' : 'positions',
            'has'    : 'note role user'.split(),
            'in'     : 'team role user'.split()
        },
        role={
            'model'  : 'Role',
            'icon'   : 'fontawesome.user-tag',
            'plural' : 'roles',
            'has'    : 'note position responsibility capacity'.split(),
            'in'     : 'position responsibility capacity'.split()
        },
        responsibility={
            'model'  : 'Responsibility',
            'icon'   : 'fontawesome.user-nurse',
            'plural' : 'responsibilities',
            'has'    : 'note role'.split(),
            'in'     : 'role'.split()
        },
        capacity={
            'model'  : 'Capacity',
            'icon'   : 'fontawesome.user-ninja',
            'plural' : 'capacities',
            'has'    : 'note role'.split(),
            'in'     : 'role'.split()
        },
        user={
            'model'  : 'User',
            'icon'   : 'fontawesome.user',
            'plural' : 'users',
            'has'    : 'note position'.split(),
            'in'     : 'position'.split()
        },
        taxonomy={
            'model'  : 'Taxonomy',
            'icon'   : 'fontawesome.tags',
            'plural' : 'taxonomies',
            'has'    : 'note taxonomy term'.split(),
            'in'     : 'taxonomy'.split()
        },
        term={
            'model'  : 'Term',
            'icon'   : 'fontawesome.tag',
            'plural' : 'terms',
            'has'    : 'note term'.split(),
            'in'     : 'taxonomy term'.split()
        },
    )
    actions = 'list view new edit report delete'.split()
    routes=(
        (  'notes',            views.NoteViewSet           ),
        (  'resources',        views.ResourceViewSet       ),
        (  'products',         views.ProductViewSet        ),
        (  'goals',            views.GoalViewSet           ),
        (  'objectives',       views.ObjectiveViewSet      ),
        (  'targets',          views.TargetViewSet         ),
        (  'strategies',       views.StrategyViewSet       ),
        (  'plans',            views.PlanViewSet           ),
        (  'phases',           views.PhaseViewSet          ),
        (  'steps',            views.StepViewSet           ),
        (  'projects',         views.ProjectViewSet        ),
        (  'tasks',            views.TaskViewSet           ),
        (  'actions',          views.ActionViewSet         ),
        (  'currencies',       views.CurrencyViewSet       ),
        (  'accounts',         views.AccountViewSet        ),
        (  'pools',            views.PoolViewSet           ),
        (  'allotments',       views.AllotmentViewSet      ),
        (  'allocations',      views.AllocationViewSet     ),
        (  'incomes',          views.IncomeViewSet         ),
        (  'expenses',         views.ExpenseViewSet        ),
        (  'assets',           views.AssetViewSet          ),
        (  'donations',        views.DonationViewSet       ),
        (  'services',         views.ServiceViewSet        ),
        (  'rentals',          views.RentalViewSet         ),
        (  'liabilities',      views.LiabilityViewSet      ),
        (  'contributions',    views.ContributionViewSet   ),
        (  'commissions',      views.CommissionViewSet     ),
        (  'employments',      views.EmploymentViewSet     ),
        (  'investments',      views.InvestmentViewSet     ),
        (  'receipts',         views.ReceiptViewSet        ),
        (  'deposits',         views.DepositViewSet        ),
        (  'payments',         views.PaymentViewSet        ),
        (  'budgets',          views.BudgetViewSet         ),
        (  'transfers',        views.TransferViewSet       ),
        (  'relocations',      views.RelocationViewSet     ),
        (  'earnings',         views.EarningViewSet        ),
        (  'purchases',        views.PurchaseViewSet       ),
        (  'teams',            views.TeamViewSet           ),
        (  'positions',        views.PositionViewSet       ),
        (  'roles',            views.RoleViewSet           ),
        (  'responsibilities', views.ResponsibilityViewSet ),
        (  'capacities',       views.CapacityViewSet       ),
        (  'users',            views.UserViewSet           ),
        (  'taxonomies',       views.TaxonomyViewSet       ),
        (  'terms',            views.TermViewSet           ),
    )
    @property
    def data( self ):
        return (
        ( '0.1.0',
          ( '#widgets', ( 'from relations', self.objects, self.relations )),
          ( '#blocks',
            ( 'form',
              ( 'basic', dict(
                  extends='form.section',
                  data=dict( fields='active name title description'.split() ))),
              ( 'extra',
                ( 'resources', dict(
                    extends='form.section',
                    data=dict( fields='url upload parent attached_to'.split() ))),
                ( 'goal', dict(
                    extends='form.section'
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
              ( 'relations',
                ( 'note', dict(
                    extends='form.section',
                    data=dict( fields='notes'.split() ))),
                ( 'resource', dict(
                    extends='form.section',
                    data=dict( fields='resources notes'.split() ))),
                ( 'product', dict(
                    extends='form.section',
                    data=dict( fields='products notes'.split() ))),
                ( 'goal', dict(
                    extends='form.section',
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
                  extends='form.calendar',
                  data=dict(
                      dates=[
                          dict( model='intrepid.Goal',
                                start='intended_start',
                                end='intended_end' ),
                          dict( model='intrepid.Goal',
                                start='actual_start',
                                end='actual_end' )]))))),
          ( '#screens',
            ( 'list',
              tuple(
                  ( o, dict(
                      extends='list.from.model',
                      data=dict(
                          model=self.relations[o][ 'model' ])))
                        for o in self.objects)),
            ( 'new',
              ( 'note', dict(
                  extends='form.single',
                  data=dict(
                      blocks=
                      ( 'slot',
                        dict( block='form.basic' ),
                        dict( block='form.relations.note' ))))),
              ( 'resource', dict(
                  extends='form.single',
                  # data=dict(
                  # blocks=
                  # ( 'slot',
                  #   dict( block='form.basic' ),
                  #   dict( block='form.extra.resource' ),
                  #   dict( block='form.relations.resource' )))
                      )),
              ( 'product', dict(
                  extends='form.single',
                  data=dict(
                      blocks=
                      ( 'slot',
                        dict( block='form.basic' ),
                        dict( block='form.extra.product' ),
                        dict( block='form.relations.product' ))))),
              ( 'goal', dict(
                  extends='form.single',
                  data=dict(
                      blocks=
                      ( 'slot',
                        dict( block='form.basic' ),
                        dict( block='form.infobox.goal' ),
                        dict( block='form.extra.goal' ),
                        dict( block='form.relations.goal' ))))),
              # ( 'objective', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.objective' ),
              #       dict( block='form.relations.objective' )))),
              # ( 'target', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.target' ),
              #       dict( block='form.relations.target' )))),
              # ( 'strategy', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.strategy' ),
              #       dict( block='form.relations.strategy' )))),
              # ( 'plan', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.plan' ),
              #       dict( block='form.relations.plan' )))),
              # ( 'phase', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.phase' ),
              #       dict( block='form.relations.phase' )))),
              # ( 'step', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.step' ),
              #       dict( block='form.relations.step' )))),
              # ( 'project', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.project' ),
              #       dict( block='form.relations.project' )))),
              # ( 'task', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.task' ),
              #       dict( block='form.relations.task' )))),
              # ( 'action', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.action' ),
              #       dict( block='form.relations.action' )))),
              # ( 'currency', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.currency' ),
              #       dict( block='form.relations.currency' )))),
              # ( 'account', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.account' ),
              #       dict( block='form.relations.account' )))),
              # ( 'pool', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.pool' ),
              #       dict( block='form.relations.pool' )))),
              # ( 'allotment', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.allotment' ),
              #       dict( block='form.relations.allotment' )))),
              # ( 'allocation', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.allocation' ),
              #       dict( block='form.relations.allocation' )))),
              # ( 'income', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.income' ),
              #       dict( block='form.relations.income' )))),
              # ( 'expense', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.expense' ),
              #       dict( block='form.relations.expense' )))),
              # ( 'asset', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.asset' ),
              #       dict( block='form.relations.asset' )))),
              # ( 'donation', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.donation' ),
              #       dict( block='form.relations.donation' )))),
              # ( 'service', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.service' ),
              #       dict( block='form.relations.service' )))),
              # ( 'rental', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.rental' ),
              #       dict( block='form.relations.rental' )))),
              # ( 'liability', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.liability' ),
              #       dict( block='form.relations.liability' )))),
              # ( 'contribution', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.contribution' ),
              #       dict( block='form.relations.contribution' )))),
              # ( 'commission', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.commission' ),
              #       dict( block='form.relations.commission' )))),
              # ( 'employment', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.employment' ),
              #       dict( block='form.relations.employment' )))),
              # ( 'investment', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.investment' ),
              #       dict( block='form.relations.investment' )))),
              # ( 'receipt', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.receipt' ),
              #       dict( block='form.relations.receipt' )))),
              # ( 'deposit', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.deposit' ),
              #       dict( block='form.relations.deposit' )))),
              # ( 'payment', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.payment' ),
              #       dict( block='form.relations.payment' )))),
              # ( 'budget', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.budget' ),
              #       dict( block='form.relations.budget' )))),
              # ( 'transfer', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.transfer' ),
              #       dict( block='form.relations.transfer' )))),
              # ( 'relocation', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.relocation' ),
              #       dict( block='form.relations.relocation' )))),
              # ( 'earning', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.earning' ),
              #       dict( block='form.relations.earning' )))),
              # ( 'purchase', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.purchase' ),
              #       dict( block='form.relations.purchase' )))),
              # ( 'team', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.team' ),
              #       dict( block='form.relations.team' )))),
              # ( 'position', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.position' ),
              #       dict( block='form.relations.position' )))),
              # ( 'role', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.role' ),
              #       dict( block='form.relations.role' )))),
              # ( 'responsibility', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.responsibility' ),
              #       dict( block='form.relations.responsibility' )))),
              # ( 'capacity', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.capacity' ),
              #       dict( block='form.relations.capacity' )))),
              # ( 'user', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.user' ),
              #       dict( block='form.relations.user' )))),
              # ( 'taxonomy', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.taxonomy' ),
              #       dict( block='form.relations.taxonomy' )))),
              # ( 'term', dict(
              #     extends='form.single',
              #     blocks=
              #     ( 'slot',
              #       dict( block='form.basic' ),
              #       dict( block='form.extra.term' ),
              #       dict( block='form.relations.term' )))),
                    ),
          ),
          ( '#locations', ( 'from relations', self.objects, self.relations )),
          ( '#settings', ( 'from relations', self.objects, self.relations )),
          ( '#links', ),
          # ( '', ),
        ),
    )

