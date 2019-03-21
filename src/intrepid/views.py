# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
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

