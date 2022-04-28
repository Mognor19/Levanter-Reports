from datetime import datetime, date, timedelta
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from .models import *
import pandas as pd
from django.contrib.auth.decorators import login_required

@login_required
def accounts(request):
    return render (request, 'reports/accounts_upload.html')

@login_required
def reports(request):
    return render(request, 'reports/accounts_reports.html')

@login_required
def reports_propio(request):
    Employees = Propio.objects.all()
    Dates = Propio_CallHistory.objects.order_by().values('interaction_date').distinct()
    Call_History = Propio_CallHistory.objects.all()
    emp_id = request.GET.getlist('employee_id')
    Date = request.GET.get('date')
    minutes = 0
    total_minutes = Propio_CallHistory.objects.aggregate(Sum('interaction_length_minutes'))
    calls = 0
    total_calls = Propio_CallHistory.objects.all().count()
    
    ctx = {
        "Employees":Employees,
        "Dates":Dates,
        "data":Call_History,
        "total_calls":total_calls,
        "total_minutes":total_minutes,
    }

    if (emp_id != []):
        ctx = {
            "Employees":Employees,
            "Dates":Dates,
        }
        for e in emp_id:
            Employee = Propio.objects.get(employee_id=e)
            Call_History = Propio_CallHistory.objects.filter(employee_id=Employee)
            total_calls = Propio_CallHistory.objects.filter(employee_id=Employee).count()
            total_minutes = Propio_CallHistory.objects.filter(employee_id=Employee).aggregate(Sum('interaction_length_minutes'))
            if (Date != None and emp_id != []):
                date_formated = datetime.strptime(Date, '%b. %d, %Y').date()
                Call_History = Propio_CallHistory.objects.filter(interaction_date=date_formated, employee_id=Employee)
                total_calls = Propio_CallHistory.objects.filter(interaction_date=date_formated, employee_id=Employee).count()
                total_minutes = Propio_CallHistory.objects.filter(interaction_date=date_formated, employee_id=Employee).aggregate(Sum('interaction_length_minutes'))
                
                if "data" in ctx:
                    ctx["data"] = ctx["data"].union(Call_History)
                else:
                    ctx["data"] = Call_History

                calls += total_calls
                minutes += total_minutes["interaction_length_minutes__sum"]
            else:
                calls += total_calls
                if "data" in ctx:
                    ctx["data"] = ctx["data"].union(Call_History)
                else:
                    ctx["data"] = Call_History
                minutes += total_minutes["interaction_length_minutes__sum"]

            ctx["total_calls"] = calls
            ctx["total_minutes"] = minutes

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
            
        return render(request, 'reports/reports_propio.html', ctx)

    return render(request, 'reports/reports_propio.html', ctx)

@login_required
def reports_transperfect(request):
    Employees = Transperfect.objects.all()
    Dates = Transperfect_CallHistory.objects.order_by().values('date').distinct()
    Call_History = Transperfect_CallHistory.objects.all()
    emp_id = request.GET.getlist('employee_id')
    Date = request.GET.get('date')
    eof_minutes = 0
    available_minutes = 0
    talk_minutes = 0
    acw_minutes = 0
    ring_through_minutes = 0
    break_minutes = 0
    schedule_call_minutes = 0
    meeting_minutes = 0
    lunch_minutes = 0
    calls = 0
    total_calls = Transperfect_CallHistory.objects.all().count()

    for ch in Call_History:
        eof_minutes += ch.eof_minutes
        available_minutes += ch.available_minutes
        talk_minutes += ch.talk_minutes
        acw_minutes += ch.acw_minutes
        ring_through_minutes += ch.ring_through_minutes
        break_minutes += ch.break_minutes
        schedule_call_minutes += ch.schedule_call_minutes
        meeting_minutes += ch.meeting_minutes
        lunch_minutes += ch.lunch_minutes
    
    ctx = {
        "Employees":Employees,
        "Dates":Dates,
        "data":Call_History,
        "total_calls":total_calls,
        "eof_minutes":round(eof_minutes,2),
        "available_minutes":round(available_minutes,2),
        "talk_minutes":round(talk_minutes,2),
        "acw_minutes":round(acw_minutes,2),
        "ring_through_minutes":round(ring_through_minutes,2),
        "break_minutes":round(break_minutes,2),
        "schedule_call_minutes":round(schedule_call_minutes,2),
        "meeting_minutes":round(meeting_minutes,2),
        "lunch_minutes":round(lunch_minutes,2),
    }

    if (emp_id != []):
        eof_minutes = 0
        available_minutes = 0
        talk_minutes = 0
        acw_minutes = 0
        ring_through_minutes = 0
        break_minutes = 0
        schedule_call_minutes = 0
        meeting_minutes = 0
        lunch_minutes = 0
        ctx = {
            "Employees":Employees,
            "Dates":Dates,
        }
        for e in emp_id:
            Employee = Transperfect.objects.get(employee_id=e)
            Call_History = Transperfect_CallHistory.objects.filter(employee_id=Employee)

            if (Date != None and emp_id != []):
                date_formated = datetime.strptime(Date, '%B %d, %Y').date()
                Call_History = Transperfect_CallHistory.objects.filter(date=date_formated, employee_id=Employee)
                total_calls = Transperfect_CallHistory.objects.filter(date=date_formated, employee_id=Employee).count()
                
                if "data" in ctx:
                    ctx["data"] = ctx["data"].union(Call_History)
                else:
                    ctx["data"] = Call_History

                for ch in Call_History:
                    eof_minutes += ch.eof_minutes
                    available_minutes += ch.available_minutes
                    talk_minutes += ch.talk_minutes
                    acw_minutes += ch.acw_minutes
                    ring_through_minutes += ch.ring_through_minutes
                    break_minutes += ch.break_minutes
                    schedule_call_minutes += ch.schedule_call_minutes
                    meeting_minutes += ch.meeting_minutes
                    lunch_minutes += ch.lunch_minutes
                
                calls += total_calls

            else:
                total_calls = Transperfect_CallHistory.objects.filter(employee_id=Employee).count()
                calls += total_calls
                if "data" in ctx:
                    ctx["data"] = ctx["data"].union(Call_History)
                else:
                    ctx["data"] = Call_History
                for ch in Call_History:
                    eof_minutes += ch.eof_minutes
                    available_minutes += ch.available_minutes
                    talk_minutes += ch.talk_minutes
                    acw_minutes += ch.acw_minutes
                    ring_through_minutes += ch.ring_through_minutes
                    break_minutes += ch.break_minutes
                    schedule_call_minutes += ch.schedule_call_minutes
                    meeting_minutes += ch.meeting_minutes
                    lunch_minutes += ch.lunch_minutes
            
            ctx["total_calls"] = calls
            ctx["eof_minutes"] = round(eof_minutes,2)
            ctx["available_minutes"] = round(available_minutes,2)
            ctx["talk_minutes"] = round(talk_minutes,2)
            ctx["acw_minutes"] = round(acw_minutes,2)
            ctx["ring_through_minutes"] = round(ring_through_minutes,2)
            ctx["break_minutes"] = round(break_minutes,2)
            ctx["schedule_call_minutes"] = round(schedule_call_minutes,2)
            ctx["meeting_minutes"] = round(meeting_minutes,2)
            ctx["lunch_minutes"] = round(lunch_minutes,2)

    elif (Date != None):
        eof_minutes = 0
        available_minutes = 0
        talk_minutes = 0
        acw_minutes = 0
        ring_through_minutes = 0
        break_minutes = 0
        schedule_call_minutes = 0
        meeting_minutes = 0
        lunch_minutes = 0

        date_formated = datetime.strptime(Date, '%B %d, %Y').date()
        Call_History = Transperfect_CallHistory.objects.filter(date=date_formated)
        total_calls = Transperfect_CallHistory.objects.filter(date=date_formated).count()

        for ch in Call_History:
            eof_minutes += ch.eof_minutes
            available_minutes += ch.available_minutes
            talk_minutes += ch.talk_minutes
            acw_minutes += ch.acw_minutes
            ring_through_minutes += ch.ring_through_minutes
            break_minutes += ch.break_minutes
            schedule_call_minutes += ch.schedule_call_minutes
            meeting_minutes += ch.meeting_minutes
            lunch_minutes += ch.lunch_minutes
        
        ctx = {
            "Employees":Employees,
            "Dates":Dates,
            "data":Call_History,
            "total_calls":total_calls,
            "eof_minutes":round(eof_minutes,2),
            "available_minutes":round(available_minutes,2),
            "talk_minutes":round(talk_minutes,2),
            "acw_minutes":round(acw_minutes,2),
            "ring_through_minutes":round(ring_through_minutes,2),
            "break_minutes":round(break_minutes,2),
            "schedule_call_minutes":round(schedule_call_minutes,2),
            "meeting_minutes":round(meeting_minutes,2),
            "lunch_minutes":round(lunch_minutes,2),

        }
            
        return render(request, 'reports/reports_transperfect.html', ctx)

    return render(request, 'reports/reports_transperfect.html', ctx)

@login_required
def employees_transperfect(request):
    date_call_history = request.POST.get('date')
    today = date.today()
    week = today - timedelta(days=7)
    
    ctx = {
        "today":today.strftime("%Y-%m-%d"),
        "week":week.strftime("%Y-%m-%d"),
    }

    if (request.method == "POST"):
        file = request.FILES['call-history']
        df=pd.read_excel(file, skiprows=2)
        for x in range(len(df["Unnamed: 1"])):
            if isinstance(df["Unnamed: 1"][x], str):
                employee = Transperfect.objects.get(transperfect_id=df["Unnamed: 1"][x])
                converted_time_str = datetime.strptime(df["unavailable - end of shift"][x], '%H:%M:%S').time()
                eof_minutes = round(((converted_time_str.hour*60)+converted_time_str.minute+(converted_time_str.second/60)),2)

                converted_time_str = datetime.strptime(df["available"][x], '%H:%M:%S').time()
                available_minutes = round(((converted_time_str.hour*60)+converted_time_str.minute+(converted_time_str.second/60)),2)

                converted_time_str = datetime.strptime(df["Talk Time"][x], '%H:%M:%S').time()
                talk_minutes = round(((converted_time_str.hour*60)+converted_time_str.minute+(converted_time_str.second/60)),2)

                converted_time_str = datetime.strptime(df["unavailable - acw"][x], '%H:%M:%S').time()
                acw_minutes = round(((converted_time_str.hour*60)+converted_time_str.minute+(converted_time_str.second/60)),2)

                converted_time_str = datetime.strptime(df["unavailable - ring-through"][x], '%H:%M:%S').time()
                ring_through_minutes = round(((converted_time_str.hour*60)+converted_time_str.minute+(converted_time_str.second/60)),2)

                converted_time_str = datetime.strptime(df["unavailable - break"][x], '%H:%M:%S').time()
                break_minutes = round(((converted_time_str.hour*60)+converted_time_str.minute+(converted_time_str.second/60)),2)

                converted_time_str = datetime.strptime(df["unavailable - scheduled call"][x], '%H:%M:%S').time()
                schedule_call_minutes = round(((converted_time_str.hour*60)+converted_time_str.minute+(converted_time_str.second/60)),2)

                converted_time_str = datetime.strptime(df["unavailable - meeting"][x], '%H:%M:%S').time()
                meeting_minutes = round(((converted_time_str.hour*60)+converted_time_str.minute+(converted_time_str.second/60)),2)

                converted_time_str = datetime.strptime(df["unavailable - lunch"][x], '%H:%M:%S').time()
                lunch_minutes = round(((converted_time_str.hour*60)+converted_time_str.minute+(converted_time_str.second/60)),2)

                calls = Transperfect_CallHistory(
                    employee_id=employee,
                    date=date_call_history,
                    shift_eof=df["unavailable - end of shift"][x],
                    eof_minutes=eof_minutes,
                    shift_available=df["available"][x],
                    available_minutes=available_minutes,
                    shift_talk_time=df["Talk Time"][x],
                    talk_minutes=talk_minutes,
                    shift_acw=df["unavailable - acw"][x],
                    acw_minutes=acw_minutes,
                    shift_ring_through=df["unavailable - ring-through"][x],
                    ring_through_minutes=ring_through_minutes,
                    shift_break=df["unavailable - break"][x],
                    break_minutes=break_minutes,
                    shift_schedule_call=df["unavailable - scheduled call"][x],
                    schedule_call_minutes=schedule_call_minutes,
                    shift_meeting=df["unavailable - meeting"][x],
                    meeting_minutes=meeting_minutes,
                    shift_lunch=df["unavailable - lunch"][x],
                    lunch_minutes=lunch_minutes,
                )
                calls.save()
        return render(request, 'reports/employee_transperfect.html', ctx)
    return render(request, 'reports/employee_transperfect.html', ctx)

@login_required
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
        return render(request, 'reports/accounts_upload.html')


    ctx = {
        "Employees": Employees,
    }
    return render(request, 'reports/employees_propio.html', ctx )

@login_required
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

@login_required
def get_employee_transperfect(request):
    Employees = Transperfect.objects.all()
    Cities = City.objects.all()
    Skillsets = Skillset.objects.get(skillset='MSI TP')

    if (request.method == "POST"):
        employee_id = request.POST.get('employee_id')
        transperfect_id = request.POST.get('transperfect_id')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_names = request.POST.get('last_names')
        city = request.POST.get('city')
        city_id = City.objects.get(city=city)
        employee = Transperfect(
            employee_id = employee_id,
            first_name  = first_name, 
            middle_name = middle_name,
            last_names = last_names,
            transperfect_id = transperfect_id,
            skillset=Skillsets,
            city=city_id,
        )
        employee.save()
        ctx = {
            "Employees":Employees,
            "Cities":Cities,
            "Skillsets":Skillsets,
        }
        return render(request, 'employees/transperfect.html', ctx)

    ctx = {
        "Employees":Employees,
        "Cities":Cities,
        "Skillsets":Skillsets,
    }
    return render(request, 'employees/transperfect.html', ctx)

@login_required
def deactivate_employee_propio(request, uid):
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

@login_required
def activate_employee_propio(request, uid):
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

@login_required
def deactivate_employee_transperfect(request, uid):
    employee = get_object_or_404(Transperfect, employee_id=uid)
    employee.employee_active = "0"
    employee.save()

    Employees = Transperfect.objects.all()
    Cities = City.objects.all()
    Skillsets = Skillset.objects.get(skillset='MSI TP')

    ctx = {
        "Employees":Employees,
        "Cities":Cities,
        "Skillsets":Skillsets,
    }
    return render(request, 'employees/transperfect.html', ctx)

@login_required
def activate_employee_transperfect(request, uid):
    employee = get_object_or_404(Transperfect, employee_id=uid)
    employee.employee_active = "1"
    employee.save()

    Employees = Transperfect.objects.all()
    Cities = City.objects.all()
    Skillsets = Skillset.objects.get(skillset='MSI TP')

    ctx = {
        "Employees":Employees,
        "Cities":Cities,
        "Skillsets":Skillsets,
    }
    return render(request, 'employees/transperfect.html', ctx)

