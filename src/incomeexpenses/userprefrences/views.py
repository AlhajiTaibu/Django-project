from django.contrib import messages
from django.shortcuts import render, redirect
import json
import os
from django.conf import settings
from .models import UserPreferences


def index(request):
    currencies = []

    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path) as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currencies.append({'name': k, 'value': v})
        context = {
            'currencies': currencies
        }

    if request.method == 'GET':
        return render(request, 'preferences/index.html', context)

    if request.method == 'POST':
        currency = request.POST['currency']
        user_preference = UserPreferences.objects.filter(user=request.user)
        if user_preference.exists():
            user_preference = UserPreferences.objects.get(user=request.user)
            user_preference.currency = currency
            user_preference.save()
            context = {
                'currencies': currencies,
                'user_preferences': user_preference
            }
            messages.success(request, 'Changes saved success')
            return render(request, 'preferences/index.html', context)
        else:
            currency_preference = UserPreferences.objects.create(
                user=request.user, currency=currency
            )
            currency_preference.save()
            messages.success(request, 'Currency preferences created successfully')
            return redirect('user-preferences')

