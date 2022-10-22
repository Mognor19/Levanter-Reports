from django.urls import path
from . import views

app_name = 'Registro'

urlpatterns = [
    
    #URLs para Subir datos
    path('record/', views.record, name='record'),

]
