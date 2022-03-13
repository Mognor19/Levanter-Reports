from django.http import JsonResponse
from django.shortcuts import render
from .models import *
import pandas as pd
import django_excel as excel

# Create your views here.

def accounts(request):
    return render (request, 'reports/accounts.html')

def reports(request):
    Call_History = Propio_CallHistory.objects.all()

    ctx = {
        "data":Call_History,
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
        # request.FILES['call-history'].save_to_database(
        #     model= Propio_CallHistory,
        #     mapdict={
        #         "interaction_date":"LABEL-3",
        #         "interaction_start_time":"LABEL-4",
        #         "interaction_length":"LABEL-5",
        #     }
        # )
        return render(request, 'reports/accounts.html')


    ctx = {
        "Employees": Employees,
    }
    return render(request, 'reports/employees_propio.html', ctx )

def get_employee_propio(request):
    Employees = Propio.objects.all()
    Eid = request.GET.get('employee')
    E = Propio.objects.filter(employee_id=Eid)

    ctx = {
        "Employees":Employees,
        "Employee":E,
        "Test":Eid,
    }
    return JsonResponse(ctx)

