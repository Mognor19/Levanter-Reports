from django.http import JsonResponse
from datetime import datetime
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from .models import *
import pandas as pd
import django_excel as excel

# Create your views here.

def accounts(request):
    return render (request, 'reports/accounts.html')

def reports(request):
    Employees = Propio.objects.all()
    Dates = Propio_CallHistory.objects.order_by().values('interaction_date').distinct()
    Call_History = Propio_CallHistory.objects.all()
    emp_id = request.GET.get('employee_id')
    Date = request.GET.get('date')
    total_minutes = Propio_CallHistory.objects.aggregate(Sum('interaction_length_minutes'))
    total_calls = Propio_CallHistory.objects.all().count()
    

    if (emp_id != None):
        Employee = Propio.objects.get(employee_id=emp_id)
        Call_History = Propio_CallHistory.objects.filter(employee_id=Employee)
        total_calls = Propio_CallHistory.objects.filter(employee_id=Employee).count()
        total_minutes = Propio_CallHistory.objects.filter(employee_id=Employee).aggregate(Sum('interaction_length_minutes'))
        if (Date != None and emp_id != None):
            date_formated = datetime.strptime(Date, '%b. %d, %Y').date()
            Call_History = Propio_CallHistory.objects.filter(interaction_date=date_formated, employee_id=Employee)
            total_calls = Propio_CallHistory.objects.filter(interaction_date=date_formated, employee_id=Employee).count()
            total_minutes = Propio_CallHistory.objects.filter(interaction_date=date_formated, employee_id=Employee).aggregate(Sum('interaction_length_minutes'))
            ctx = {
                "Employees":Employees,
                "Dates":Dates,
                "data":Call_History,
                "total_calls":total_calls,
                "total_minutes":total_minutes,
            }
            
            return render(request, 'reports/reports.html', ctx)
        ctx = {
            "Employees":Employees,
            "Dates":Dates,
            "data":Call_History,
            "total_calls":total_calls,
            "total_minutes":total_minutes,
        }
        
        return render(request, 'reports/reports.html', ctx)
    elif (Date != None):
        date_formated = datetime.strptime(Date, '%b. %d, %Y').date()
        Call_History = Propio_CallHistory.objects.filter(interaction_date=date_formated)
        total_calls = Propio_CallHistory.objects.filter(interaction_date=date_formated).count()
        total_minutes = Propio_CallHistory.objects.filter(interaction_date=date_formated).aggregate(Sum('interaction_length_minutes'))
        ctx = {
            "Employees":Employees,
            "Dates":Dates,
            "data":Call_History,
            "total_calls":total_calls,
            "total_minutes":total_minutes,
        }
            
        return render(request, 'reports/reports.html', ctx)

    ctx = {
        "Employees":Employees,
        "Dates":Dates,
        "data":Call_History,
        "total_calls":total_calls,
        "total_minutes":total_minutes,
    }
    return render(request, 'reports/reports.html', ctx)

def employees_propio(request):
    Employees = Propio.objects.all()

    if (request.method == "POST"):
        emp_id = request.POST.get('employee')
        employee = Propio.objects.get(employee_id=emp_id)
        file = request.FILES['call-history']
        df=pd.read_excel(file)
        df.columns=["LABEL-1","LABEL-2","LABEL-3", "LABEL-4", "LABEL-5","LABEL-6","LABEL-7"]
        for x in range(len(df["LABEL-1"])):
            if(((df["LABEL-5"][x].hour * 60) + df["LABEL-5"][x].minute)<10):
                minute = df["LABEL-5"][x].minute 
                lenght = f'00:0{minute}:00'
            elif (((df["LABEL-5"][x].hour * 60) + df["LABEL-5"][x].minute)<60):
                minutes = (df["LABEL-5"][x].hour * 60) + df["LABEL-5"][x].minute 
                lenght = f'00:{minutes}:00'
            elif ((((df["LABEL-5"][x].hour * 60) + df["LABEL-5"][x].minute)<60 and df["LABEL-5"][x].minute)<10) :
                hours = df["LABEL-5"][x].hour
                minutes = df["LABEL-5"][x].minute
                lenght = f'0{hours}:0{minutes}:00'
            else: 
                hours = df["LABEL-5"][x].hour
                minutes = df["LABEL-5"][x].minute
                lenght = f'0{hours}:{minutes}:00'
            calls = Propio_CallHistory(
                employee_id = employee,
                interaction_date  = df["LABEL-3"][x], 
                interaction_start_time = df["LABEL-4"][x],
                interaction_length = lenght,
                interaction_length_minutes = ((df["LABEL-5"][x].hour * 60) + df["LABEL-5"][x].minute),
            )
            calls.save()
        return render(request, 'reports/accounts.html')


    ctx = {
        "Employees": Employees,
    }
    return render(request, 'reports/employees_propio.html', ctx )

def get_employee_propio(request):
    Employees = Propio.objects.all()
    Cities = City.objects.all()
    Skillsets = Skillset.objects.get(skillset='MSI PR')

    if (request.method == "POST"):
        employee_id = request.POST.get('employee_id')
        propio_id = request.POST.get('propio_id')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_names = request.POST.get('last_names')
        city = request.POST.get('city')
        city_id = City.objects.get(city=city)
        employee = Propio(
            employee_id = employee_id,
            first_name  = first_name, 
            middle_name = middle_name,
            last_names = last_names,
            propio_id = propio_id,
            skillset=Skillsets,
            city=city_id,
        )
        employee.save()
        ctx = {
            "Employees":Employees,
            "Cities":Cities,
            "Skillsets":Skillsets,
        }
        return render(request, 'employees/propio.html', ctx)

    ctx = {
        "Employees":Employees,
        "Cities":Cities,
        "Skillsets":Skillsets,
    }
    return render(request, 'employees/propio.html', ctx)


def deactivate_employee(request, uid):
    employee = get_object_or_404(Propio, employee_id=uid)
    employee.employee_active = "0"
    employee.save()

    Employees = Propio.objects.all()
    Cities = City.objects.all()
    Skillsets = Skillset.objects.get(skillset='MSI PR')

    ctx = {
        "Employees":Employees,
        "Cities":Cities,
        "Skillsets":Skillsets,
    }
    return render(request, 'employees/propio.html', ctx)


def activate_employee(request, uid):
    employee = get_object_or_404(Propio, employee_id=uid)
    employee.employee_active = "1"
    employee.save()

    Employees = Propio.objects.all()
    Cities = City.objects.all()
    Skillsets = Skillset.objects.get(skillset='MSI PR')

    ctx = {
        "Employees":Employees,
        "Cities":Cities,
        "Skillsets":Skillsets,
    }
    return render(request, 'employees/propio.html', ctx)

