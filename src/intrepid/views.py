# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
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

class NoteSerializer( viewsets.ModelViewSet ):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class ResourceSerializer( viewsets.ModelViewSet ):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class ProductSerializer( viewsets.ModelViewSet ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class GoalSerializer( viewsets.ModelViewSet ):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer


class ObjectiveSerializer( viewsets.ModelViewSet ):
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer


class TargetSerializer( viewsets.ModelViewSet ):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer


class StrategySerializer( viewsets.ModelViewSet ):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer


class PlanSerializer( viewsets.ModelViewSet ):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class PhaseSerializer( viewsets.ModelViewSet ):
    queryset = Phase.objects.all()
    serializer_class = PhaseSerializer


class StepSerializer( viewsets.ModelViewSet ):
    queryset = Step.objects.all()
    serializer_class = StepSerializer


class ProjectSerializer( viewsets.ModelViewSet ):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TaskSerializer( viewsets.ModelViewSet ):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ActionSerializer( viewsets.ModelViewSet ):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class CurrencySerializer( viewsets.ModelViewSet ):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class AccountSerializer( viewsets.ModelViewSet ):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class PoolSerializer( viewsets.ModelViewSet ):
    queryset = Pool.objects.all()
    serializer_class = PoolSerializer


class AllotmentSerializer( viewsets.ModelViewSet ):
    queryset = Allotment.objects.all()
    serializer_class = AllotmentSerializer


class AllocationSerializer( viewsets.ModelViewSet ):
    queryset = Allocation.objects.all()
    serializer_class = AllocationSerializer


class IncomeSerializer( viewsets.ModelViewSet ):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


class ExpenseSerializer( viewsets.ModelViewSet ):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class AssetSerializer( viewsets.ModelViewSet ):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class DonationSerializer( viewsets.ModelViewSet ):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer


class ServiceSerializer( viewsets.ModelViewSet ):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class RentalSerializer( viewsets.ModelViewSet ):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer


class SourceSerializer( viewsets.ModelViewSet ):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class LiabilitySerializer( viewsets.ModelViewSet ):
    queryset = Liability.objects.all()
    serializer_class = LiabilitySerializer


class ContributionSerializer( viewsets.ModelViewSet ):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer


class CommissionSerializer( viewsets.ModelViewSet ):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer


class EmploymentSerializer( viewsets.ModelViewSet ):
    queryset = Employment.objects.all()
    serializer_class = EmploymentSerializer


class InvestmentSerializer( viewsets.ModelViewSet ):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer


class ReceiptSerializer( viewsets.ModelViewSet ):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer


class DepositSerializer( viewsets.ModelViewSet ):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer


class PaymentSerializer( viewsets.ModelViewSet ):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class BudgetSerializer( viewsets.ModelViewSet ):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer


class LineSerializer( viewsets.ModelViewSet ):
    queryset = Line.objects.all()
    serializer_class = LineSerializer


class TransferSerializer( viewsets.ModelViewSet ):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer


class RelocationSerializer( viewsets.ModelViewSet ):
    queryset = Relocation.objects.all()
    serializer_class = RelocationSerializer


class EarningSerializer( viewsets.ModelViewSet ):
    queryset = Earning.objects.all()
    serializer_class = EarningSerializer


class PurchaseSerializer( viewsets.ModelViewSet ):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


class TeamSerializer( viewsets.ModelViewSet ):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PositionSerializer( viewsets.ModelViewSet ):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class RoleSerializer( viewsets.ModelViewSet ):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class ResponsibilitySerializer( viewsets.ModelViewSet ):
    queryset = Responsibility.objects.all()
    serializer_class = ResponsibilitySerializer


class CapacitySerializer( viewsets.ModelViewSet ):
    queryset = Capacity.objects.all()
    serializer_class = CapacitySerializer


class UserSerializer( viewsets.ModelViewSet ):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TaxonomySerializer( viewsets.ModelViewSet ):
    queryset = Taxonomy.objects.all()
    serializer_class = TaxonomySerializer


class TermSerializer( viewsets.ModelViewSet ):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
