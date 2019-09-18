# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import status, viewsets, permissions, filters
from aries.views import OwnedViewMixin
from .serializers import *

### route views

def index( request ):
    return render( request, 'intrepid/index.html' )

def goals( request ):
    return render( request, 'intrepid/goals.html' )

def goal( request, _id ):
    return render( request, 'intrepid/goal.html' )

def objective( request, _id ):
    return render( request, 'intrepid/objective.html' )

def target( request, _id ):
    return render( request, 'intrepid/target.html' )

def strategy( request, _id ):
    return render( request, 'intrepid/strategy.html' )

def plan( request, _id ):
    return render( request, 'intrepid/plan.html' )

def projects( request, goal=None ):
    return render( request, 'intrepid/projects.html' )

def project( request, _id ):
    return render( request, 'intrepid/project.html' )

def tasks( request, project=None ):
    return render( request, 'intrepid/tasks.html' )

def task( request, _id ):
    return render( request, 'intrepid/task.html' )

def currencios( request ):
    return render( request, 'intrepid/currencios.html' )

def accounts( request ):
    return render( request, 'intrepid/accounts.html' )

def account( request, _id ):
    return render( request, 'intrepid/account.html' )

def externals( request ):
    return render( request, 'intrepid/externals.html' )

def incomes( request ):
    return render( request, 'intrepid/incomes.html' )

def income( request, _id ):
    return render( request, 'intrepid/income.html' )

def expenses( request ):
    return render( request, 'intrepid/expenses.html' )

def expenses( request, _id ):
    return render( request, 'intrepid/expenses.html' )

def budgets( request ):
    return render( request, 'intrepid/budgets.html' )

def budget( request, _id ):
    return render( request, 'intrepid/budget.html' )

def transactions( request ):
    return render( request, 'intrepid/transactions.html' )

def transaction( request, _id ):
    return render( request, 'intrepid/transaction.html' )

def teams( request ):
    return render( request, 'intrepid/teams.html' )

def team( request, _id ):
    return render( request, 'intrepid/team.html' )

### rest api views

class IdsFilter( filters.BaseFilterBackend ):
    """
    Filter for retrieving multiple objects by ID
    """
    def filter_queryset( self, request, queryset, view ):
        ids = request.query_params.get( 'ids' )
        if not ids:
            return queryset
        try:
            ids = [ int(x) for x in ids.split(',') if len(x) ]
        except Exception:
            raise ValidationError( "Only comma-separated list of IDs for ids filter" )
        if len( ids ):
            return queryset.filter( pk__in=ids )
        return queryset


class SearchViewSet( viewsets.ModelViewSet ):
    filter_backends = ( IdsFilter, filters.SearchFilter, )
    search_fields = ( 'name', 'title', 'description' )


class BaseViewSet( OwnedViewMixin, SearchViewSet, viewsets.ModelViewSet ):
    pass


class NoteViewSet( BaseViewSet ):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class ResourceViewSet( BaseViewSet ):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class ProductViewSet( BaseViewSet ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class GoalViewSet( BaseViewSet ):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer


class ObjectiveViewSet( BaseViewSet ):
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer


class TargetViewSet( BaseViewSet ):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer


class StrategyViewSet( BaseViewSet ):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer


class PlanViewSet( BaseViewSet ):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class PhaseViewSet( BaseViewSet ):
    queryset = Phase.objects.all()
    serializer_class = PhaseSerializer


class StepViewSet( BaseViewSet ):
    queryset = Step.objects.all()
    serializer_class = StepSerializer


class ProjectViewSet( BaseViewSet ):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TaskViewSet( BaseViewSet ):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ActionViewSet( BaseViewSet ):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class CurrencyViewSet( BaseViewSet ):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class AccountViewSet( BaseViewSet ):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class PoolViewSet( BaseViewSet ):
    queryset = Pool.objects.all()
    serializer_class = PoolSerializer


class AllotmentViewSet( BaseViewSet ):
    queryset = Allotment.objects.all()
    serializer_class = AllotmentSerializer


class AllocationViewSet( BaseViewSet ):
    queryset = Allocation.objects.all()
    serializer_class = AllocationSerializer


class IncomeViewSet( BaseViewSet ):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


class ExpenseViewSet( BaseViewSet ):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class AssetViewSet( BaseViewSet ):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class DonationViewSet( BaseViewSet ):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer


class ServiceViewSet( BaseViewSet ):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class RentalViewSet( BaseViewSet ):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer


class LiabilityViewSet( BaseViewSet ):
    queryset = Liability.objects.all()
    serializer_class = LiabilitySerializer


class ContributionViewSet( BaseViewSet ):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer


class CommissionViewSet( BaseViewSet ):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer


class EmploymentViewSet( BaseViewSet ):
    queryset = Employment.objects.all()
    serializer_class = EmploymentSerializer


class InvestmentViewSet( BaseViewSet ):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer


class ReceiptViewSet( BaseViewSet ):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer


class DepositViewSet( BaseViewSet ):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer


class PaymentViewSet( BaseViewSet ):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class BudgetViewSet( BaseViewSet ):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer


class LineViewSet( BaseViewSet ):
    queryset = Line.objects.all()
    serializer_class = LineSerializer


class TransferViewSet( BaseViewSet ):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer


class RelocationViewSet( BaseViewSet ):
    queryset = Relocation.objects.all()
    serializer_class = RelocationSerializer


class EarningViewSet( BaseViewSet ):
    queryset = Earning.objects.all()
    serializer_class = EarningSerializer


class PurchaseViewSet( BaseViewSet ):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


class TeamViewSet( BaseViewSet ):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PositionViewSet( BaseViewSet ):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class RoleViewSet( BaseViewSet ):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class ResponsibilityViewSet( BaseViewSet ):
    queryset = Responsibility.objects.all()
    serializer_class = ResponsibilitySerializer


class CapacityViewSet( BaseViewSet ):
    queryset = Capacity.objects.all()
    serializer_class = CapacitySerializer


class TaxonomyViewSet( BaseViewSet ):
    queryset = Taxonomy.objects.all()
    serializer_class = TaxonomySerializer


class TermViewSet( BaseViewSet ):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
