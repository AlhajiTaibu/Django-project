from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name='income_index'),
    path('add_income', views.add_income, name='add_income'),
    path('search-income', csrf_exempt(views.search_income), name='search_income'),
    path('delete_income/<int:id>/', views.delete_income, name='delete_income'),
    path('edit_income/<int:id>/', views.detail, name='edit_income'),
]