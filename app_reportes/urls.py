from unicodedata import name
from django.urls import path
from . import views

app_name = 'Reportes'

urlpatterns = [
    
    path('', views.accounts, name='accounts'),
    path('reports/', views.reports, name='reports'),
    path('employees-propio/', views.employees_propio, name='emp_propio'),
    
    #URLs para Propio
    path('propio/', views.get_employee_propio ,name='propio'),
    path('propio/activate/<int:uid>/', views.activate_employee, name='activate_employee'),
    path('propio/deactivate/<int:uid>/', views.deactivate_employee, name='deactivate_employee'),
]
