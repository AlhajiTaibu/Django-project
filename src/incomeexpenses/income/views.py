import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Source, Income
from django.core.paginator import Paginator
from userprefrences.models import UserPreferences


def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = Income.objects.filter(
            amount__istartswith=search_str,
            owner=request.user
        ) | Income.objects.filter(date__istartswith=search_str,
                                  owner=request.user) | Income.objects.filter(
            description__icontains=search_str,
            owner=request.user
        ) | Income.objects.filter(
            source__icontains=search_str,
            owner=request.user
        )
        data = income.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    incomes = Income.objects.filter(owner=request.user)
    paginator = Paginator(incomes, 10)
    page_number = request.GET.get('page')
    page_object = Paginator.get_page(paginator, page_number)
    currency = UserPreferences.objects.get(user=request.user)
    context = {
        'incomes': incomes,
        'page_obj': page_object,
        'currency': currency
    }
    return render(request, 'income/index.html', context)


def detail(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'income/edit.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income-date']
        source = request.POST['source']
        income = Income.objects.get(pk=id)

        if income:
            if not amount:
                messages.error(request, 'Amount is required')
                return render(request, 'income/edit.html', context)
            if not description:
                messages.error(request, 'Description is required')
                return render(request, 'income/edit.html', context)
            if not date:
                messages.error(request, 'Enter a valid date')
                return render(request, 'income/edit.html', context)
            income.amount = amount
            income.description = description
            income.date = date
            income.source = source
            income.save()
            messages.success(request, 'Income edited successfully')
            return redirect('income_index')
        messages.error(request, 'Income does not exist')
        return redirect('income_index')


def delete_income(request, id):
    if request.method == 'GET':
        income = Income.objects.get(pk=id)
        income.delete()
        messages.info(request, 'Income deleted successfully')
        return redirect('income_index')
    return render(request, 'income/index.html')


def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }

    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)
        description = request.POST['description']
        date = request.POST['income-date']
        source = request.POST['source']
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context)
        if not date:
            messages.error(request, 'Enter a valid date')
            return render(request, 'income/add_income.html', context)
        income = Income.objects.create(amount=amount,
                                       description=description,
                                       date=date,
                                       source=source,
                                       owner=request.user
                                       )
        income.save()
        messages.success(request, 'Income created successfully')
        return redirect('income_index')
    return render(request, 'income/add_income.html', context)
