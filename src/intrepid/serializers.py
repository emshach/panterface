# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers as S
from aries.serializers import OwnedMixin
from .models import *

class F:
    base   = ( 'url', 'id', 'name', 'title', 'description', 'active', 'valid' )
    noted  = base + ( 'notes', )
    res    = ( 'definition', 'uri', 'upload', 'parent', 'notes', 'attached_to' )
    date   = ( 'intended_start', 'actual_start', 'intended_end', 'actual_end',
              'progress' )
    plan   = ( 'intended_start', 'actual_start', 'intended_end', 'actual_end' )
    sink   = ( 'cost', 'expense' )
    source = ( 'gain', 'destination' )

class BaseSerializer( OwnedMixin, S.HyperlinkedModelSerializer ):
    pass


class NoteSerializer( BaseSerializer ):
    class Meta:
        model = Note
        fields = F.noted


class ResourceSerializer( BaseSerializer ):
    class Meta:
        model = Resource
        fields = F.noted + F.res


class ProductSerializer( BaseSerializer ):
    class Meta:
        model = Product
        fields = F.noted + F.res


class GoalSerializer( BaseSerializer ):
    precedes = S.PrimaryKeyRelatedField(
        required=False, queryset=Goal.objects.all() )
    class Meta:
        model = Goal
        fields = F.noted + F.plan + ( 'status', 'follows', 'precedes' )


class ObjectiveSerializer( BaseSerializer ):
    class Meta:
        model = Objective
        fields = F.noted + F.plan + ( 'status', 'precedes', 'follows', 'goal',
                                      'satisfies' )


class TargetSerializer( BaseSerializer ):
    class Meta:
        model = Target
        fields = F.noted + ( 'status', 'objective', 'satisfies', 'requires',
                             'releases' )


class StrategySerializer( BaseSerializer ):
    class Meta:
        model = Strategy
        fields = F.noted + ( 'objective', )


class PlanSerializer( BaseSerializer ):
    class Meta:
        model = Plan
        fields = F.noted + F.plan + ( 'strategy', )


class PhaseSerializer( BaseSerializer ):
    class Meta:
        model = Phase
        fields = F.noted + F.plan + ( 'plan', )


class StepSerializer( BaseSerializer ):
    class Meta:
        model = Step
        fields = F.noted + F.plan + ( 'phase', )


class ProjectSerializer( BaseSerializer ):
    class Meta:
        model = Project
        fields = F.noted + F.plan + ( 'objective', 'satisfies', 'strategies',
                                      'targets' )


class TaskSerializer( BaseSerializer ):
    class Meta:
        model = Task
        fields = F.noted + F.plan + ( 'parent', 'project', 'step' )


class ActionSerializer( BaseSerializer ):
    class Meta:
        model = Action
        fields = F.noted + F.plan + ( 'follows', 'precedes', 'task' )


class CurrencySerializer( BaseSerializer ):
    class Meta:
        model = Currency
        fields = F.noted + ( 'rate', )


class AccountSerializer( BaseSerializer ):
    class Meta:
        model = Account
        fields = F.noted + ( 'amount', 'opened', 'closed', 'currency', 'allotments' )


class PoolSerializer( BaseSerializer ):
    class Meta:
        model = Pool
        fields = F.noted + ( 'size', 'available', 'parent', 'accounts', 'allotments' )


class AllotmentSerializer( BaseSerializer ):
    class Meta:
        model = Allotment
        fields = F.noted + ( 'amount', 'account', 'pool' )


class AllocationSerializer( BaseSerializer ):
    class Meta:
        model = Allocation
        fields = F.noted + ( 'opened', 'used', 'closed', 'size', 'available', 'pool' )


class IncomeSerializer( BaseSerializer ):
    class Meta:
        model = Income
        fields = F.noted + F.plan + ( 'stable', 'amount', 'sources' )


class ExpenseSerializer( BaseSerializer ):
    class Meta:
        model = Expense
        fields = F.noted + F.plan + ( 'stable', 'amount', 'source' )

class AssetSerializer( BaseSerializer ):
    class Meta:
        model = Asset
        fields = F.noted + ( 'cost', 'expense', 'value', 'intended_own',
                             'effective_own' )


class DonationSerializer( BaseSerializer ):
    class Meta:
        model = Donation
        fields = F.noted + F.sink


class ServiceSerializer( BaseSerializer ):
    class Meta:
        model = Service
        fields = F.noted + F.sink + ( 'intended', 'effective' )


class RentalSerializer( BaseSerializer ):
    class Meta:
        model = Rental
        fields = F.noted + F.sink + ( 'period', )


class LiabilitySerializer( BaseSerializer ):
    class Meta:
        model = Liability
        fields = F.noted + F.source + ( 'value', )


class ContributionSerializer( BaseSerializer ):
    class Meta:
        model = Contribution
        fields = F.noted + F.source


class CommissionSerializer( BaseSerializer ):
    class Meta:
        model = Commission
        fields = F.noted + F.source + ( 'intended_close', 'effective_close' )


class EmploymentSerializer( BaseSerializer ):
    class Meta:
        model = Employment
        fields = F.noted + F.date + F.source + ( 'period', )


class InvestmentSerializer( BaseSerializer ):
    class Meta:
        model = Investment
        fields = F.noted + F.source


class ReceiptSerializer( BaseSerializer ):
    class Meta:
        model = Receipt
        fields = F.noted + ( 'amount', 'intended', 'effective', 'income',
                             'source', 'destinations', 'deposits' )


class DepositSerializer( BaseSerializer ):
    class Meta:
        model = Deposit
        fields = F.noted + ( 'amount', 'account', 'receipt' )


class PaymentSerializer( BaseSerializer ):
    class Meta:
        model = Payment
        fields = F.noted + ( 'amount', 'intended', 'effective', 'expense',
                             'destination' )


class BudgetSerializer( BaseSerializer ):
    class Meta:
        model = Budget
        fields = F.noted + ( 'start', 'end', 'master', 'parts', 'follows',
                             'precedes' )


class LineSerializer( BaseSerializer ):
    class Meta:
        model = Line
        fields = F.noted + ( 'amount', 'intended', 'effective', 'budget' )


class TransferSerializer( BaseSerializer ):
    class Meta:
        model = Transfer
        fields = F.noted + ( 'source', 'destination' )


class RelocationSerializer( BaseSerializer ):
    class Meta:
        model = Relocation
        fields = F.noted + ( 'source', 'destination' )


class EarningSerializer( BaseSerializer ):
    class Meta:
        model = Earning
        fields = F.noted + ( 'receipt', )


class PurchaseSerializer( BaseSerializer ):
    class Meta:
        model = Purchase
        fields = F.noted + ( 'payment', )


class TeamSerializer( BaseSerializer ):
    class Meta:
        model = Team
        fields = F.noted + ( 'parent', )


class PositionSerializer( BaseSerializer ):
    class Meta:
        model = Position
        fields = F.noted + ( 'team', )


class RoleSerializer( BaseSerializer ):
    class Meta:
        model = Role
        fields = F.noted + ( 'positions', )


class ResponsibilitySerializer( BaseSerializer ):
    class Meta:
        model = Responsibility
        fields = F.noted + ( 'roles', )


class CapacitySerializer( BaseSerializer ):
    class Meta:
        model = Capacity
        fields = F.noted + ( 'roles', )


class TaxonomySerializer( BaseSerializer ):
    class Meta:
        model = Taxonomy
        fields = F.noted + ( 'hierarhichal', 'exclusive', 'parent' )


class TermSerializer( BaseSerializer ):
    class Meta:
        model = Term
        fields = F.noted + ( 'parent', 'children', 'data' )


by_model = dict(
    note=           NoteSerializer,
    resounce=       ResourceSerializer,
    product=        ProductSerializer,
    goal=           GoalSerializer,
    objective=      ObjectiveSerializer,
    target=         TargetSerializer,
    strategy=       StrategySerializer,
    plane=          PlanSerializer,
    phase=          PhaseSerializer,
    step=           StepSerializer,
    project=        ProjectSerializer,
    task=           TaskSerializer,
    action=         ActionSerializer,
    currency=       CurrencySerializer,
    account=        AccountSerializer,
    pool=           PoolSerializer,
    allotment=      AllotmentSerializer,
    allocation=     AllocationSerializer,
    income=         IncomeSerializer,
    expense=        ExpenseSerializer,
    asset=          AssetSerializer,
    donation=       DonationSerializer,
    service=        ServiceSerializer,
    rental=         RentalSerializer,
    liability=      LiabilitySerializer,
    contribution=   ContributionSerializer,
    commission=     CommissionSerializer,
    employment=     EmploymentSerializer,
    investment=     InvestmentSerializer,
    receipt=        ReceiptSerializer,
    deposit=        DepositSerializer,
    payment=        PaymentSerializer,
    budget=         BudgetSerializer,
    line=           LineSerializer,
    transfer=       TransferSerializer,
    relocation=     RelocationSerializer,
    earning=        EarningSerializer,
    purchase=       PurchaseSerializer,
    team=           TeamSerializer,
    position=       PositionSerializer,
    role=           RoleSerializer,
    responsibility= ResponsibilitySerializer,
    capacity=       CapacitySerializer,
    taxonomy=       TaxonomySerializer,
    term=           TermSerializer,
)
