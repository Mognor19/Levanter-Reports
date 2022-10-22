from django.urls import path
from . import views

app_name = 'Reportes'

urlpatterns = [
    
    #URLs para Subir datos
    path('', views.accounts, name='accounts_upload'),
    path('upload_transperfect', views.transperfect, name='transperfect_upload'),
    path('employees-propio/', views.employees_propio, name='emp_propio'),
    path('employees-transperfect/performance', views.employees_transperfect_performance, name='emp_transp_perf'),
    path('employees-transperfect/production', views.employees_transperfect_production, name='emp_transp_prod'),

    #URLs para los Reportes
    path('reports/', views.reports, name='reports'),
    path('reports_propio/', views.reports_propio, name='reports_propio'),
    path('reports_transperfect/', views.reports_transperfect, name='reports_transperfect'),
    path('reports_transperfect_performance/', views.reports_transperfect_performance, name='reports_transperfect_perf'),
    path('reports_transperfect_production/', views.reports_transperfect_production, name='reports_transperfect_prod'),
    
    #URLs para Empleados de Propio
    path('propio/', views.get_employee_propio ,name='propio'),
    path('propio/activate/<int:uid>/', views.activate_employee_propio, name='activate_employee_propio'),
    path('propio/deactivate/<int:uid>/', views.deactivate_employee_propio, name='deactivate_employee_propio'),

    #URLs para Empleados de Transperfect
    path('transperfect/', views.get_employee_transperfect ,name='transperfect'),
    path('transperfect/activate/<int:uid>/', views.activate_employee_transperfect, name='activate_employee_transperfect'),
    path('transperfect/deactivate/<int:uid>/', views.deactivate_employee_transperfect, name='deactivate_employee_transperfect'),
]
