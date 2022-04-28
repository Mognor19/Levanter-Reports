from unicodedata import name
from django.urls import path
from . import views

app_name = 'Reportes'

urlpatterns = [
    
    path('', views.accounts, name='accounts_upload'),
    path('reports/', views.reports, name='reports'),
    path('reports_propio/', views.reports_propio, name='reports_propio'),
    path('reports_transperfect/', views.reports_transperfect, name='reports_transperfect'),
    path('employees-propio/', views.employees_propio, name='emp_propio'),
    path('employees-transperfect/', views.employees_transperfect, name='emp_transp'),
    
    #URLs para Empleados de Propio
    path('propio/', views.get_employee_propio ,name='propio'),
    path('propio/activate/<int:uid>/', views.activate_employee_propio, name='activate_employee_propio'),
    path('propio/deactivate/<int:uid>/', views.deactivate_employee_propio, name='deactivate_employee_propio'),

    #URLs para Empleados de Transperfect
    path('transperfect/', views.get_employee_transperfect ,name='transperfect'),
    path('transperfect/activate/<int:uid>/', views.activate_employee_transperfect, name='activate_employee_transperfect'),
    path('transperfect/deactivate/<int:uid>/', views.deactivate_employee_transperfect, name='deactivate_employee_transperfect'),
]
