# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import views, serializers
from friede import app

class App( app.App ):
    name        =  'intrepid'
    icon        = 'fontawesome.gem'
    module      = 'intrepid'
    title       = 'Project Intrepid'
    description = '''Time, task and finance management system

    Also includes goal-setting, strategizing, and teamwork tools.'''
    min_version = '0.1.0'
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
    serializers=(
        (  'note',            serializers.NoteSerializer           ),
        (  'resource',        serializers.ResourceSerializer       ),
        (  'product',         serializers.ProductSerializer        ),
        (  'goal',            serializers.GoalSerializer           ),
        (  'objective',       serializers.ObjectiveSerializer      ),
        (  'target',          serializers.TargetSerializer         ),
        (  'strategy',        serializers.StrategySerializer       ),
        (  'plan',            serializers.PlanSerializer           ),
        (  'phase',           serializers.PhaseSerializer          ),
        (  'step',            serializers.StepSerializer           ),
        (  'project',         serializers.ProjectSerializer        ),
        (  'task',            serializers.TaskSerializer           ),
        (  'action',          serializers.ActionSerializer         ),
        (  'currency',        serializers.CurrencySerializer       ),
        (  'account',         serializers.AccountSerializer        ),
        (  'pool',            serializers.PoolSerializer           ),
        (  'allotment',       serializers.AllotmentSerializer      ),
        (  'allocation',      serializers.AllocationSerializer     ),
        (  'income',          serializers.IncomeSerializer         ),
        (  'expense',         serializers.ExpenseSerializer        ),
        (  'asset',           serializers.AssetSerializer          ),
        (  'donation',        serializers.DonationSerializer       ),
        (  'service',         serializers.ServiceSerializer        ),
        (  'rental',          serializers.RentalSerializer         ),
        (  'liability',       serializers.LiabilitySerializer      ),
        (  'contribution',    serializers.ContributionSerializer   ),
        (  'commission',      serializers.CommissionSerializer     ),
        (  'employment',      serializers.EmploymentSerializer     ),
        (  'investment',      serializers.InvestmentSerializer     ),
        (  'receipt',         serializers.ReceiptSerializer        ),
        (  'deposit',         serializers.DepositSerializer        ),
        (  'payment',         serializers.PaymentSerializer        ),
        (  'budget',          serializers.BudgetSerializer         ),
        (  'transfer',        serializers.TransferSerializer       ),
        (  'relocation',      serializers.RelocationSerializer     ),
        (  'earning',         serializers.EarningSerializer        ),
        (  'purchase',        serializers.PurchaseSerializer       ),
        (  'team',            serializers.TeamSerializer           ),
        (  'position',        serializers.PositionSerializer       ),
        (  'role',            serializers.RoleSerializer           ),
        (  'responsibility',  serializers.ResponsibilitySerializer ),
        (  'capacity',        serializers.CapacitySerializer       ),
        (  'user',            serializers.UserSerializer           ),
        (  'taxonomy',        serializers.TaxonomySerializer       ),
        (  'term',            serializers.TermSerializer           ),
    )
    @property
    def data( self ):
        return (
        ( '0.1.0',
          ( '#widgets', ( 'from relations', self.objects, self.relations )),
          ( '#locations',
            ( 'projects', dict( title="Projects", href='/projects' )),

            ( 'from relations', self.objects, self.relations )),
          ( '#settings', ( 'from relations', self.objects, self.relations )),
          ( '#links',
            ( 'menu.nav',
              ( 'projects', dict(
                  title='Projects',
                  icon='fontawesome.project-diagram',
                  location='projects' )),
            ),
          ),
          # ( '', ),
        ),
    )

