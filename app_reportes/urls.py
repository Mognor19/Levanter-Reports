from unicodedata import name
from django.urls import path
from . import views

app_name = 'Reportes'

urlpatterns = [
    
    path('', views.accounts, name='accounts'),
    path('reports/', views.reports, name='reports'),
    path('employees-propio/', views.employees_propio, name='emp_propio'),
    # path('employees-propio/get-employee/', views.get_employee_propio, name='get_emp_propio')
]
