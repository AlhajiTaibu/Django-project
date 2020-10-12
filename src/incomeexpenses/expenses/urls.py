from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name='index'),
    path('add_expenses', views.add_expenses, name='add_expenses'),
    path('search-expenses', csrf_exempt(views.search_expenses), name='search_expenses'),
    path('delete_expenses/<int:id>/', views.delete_expenses, name='delete_expenses'),
    path('edit_expenses/<int:id>/', views.detail, name='edit_expenses'),
    path('expense-summary', views.expense_category_summary, name='expense-summary'),
    path('stats', views.statsView, name='stats'),
    path('export-csv', views.export_csv, name='export-csv'),
    path('export-excel', views.export_excel, name='export-excel'),
    # path('export-pdf', views.export_pdf, name='export-pdf'),
]