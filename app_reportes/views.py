from datetime import datetime, date, timedelta, time, timezone
import pytz
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
import pandas as pd
import numpy as np
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def accounts(request):
    request.session['name'] = 'cookie'
    return render (request, 'reports/accounts_upload.html')

@login_required
def transperfect(request):
    session = request.session['name']
    return render (request, 'reports/transperfect_upload.html')

@login_required
def reports(request):
    return render(request, 'reports/accounts_reports.html')

@login_required
def reports_propio(request):
    Employees = Propio.objects.all()
    Dates = Propio_CallHistory.objects.order_by().values('interaction_date').distinct()
    Cities = City.objects.all()
    Call_History = Propio_CallHistory.objects.all()
    emp_id = request.GET.getlist('employee_id')
    Date = request.GET.getlist('date')
    city = request.GET.getlist('city')
    minutes = 0
    total_minutes = Propio_CallHistory.objects.aggregate(Sum('interaction_length_minutes'))
    calls = 0
    total_calls = Propio_CallHistory.objects.all().count()
    times = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for c in Call_History:
        times[c.interaction_start_time.hour] += 1

    ctx = {
        "Employees":Employees,
        "Dates":Dates,
        "Cities":Cities,
        "data":Call_History,
        "total_calls":total_calls,
        "total_minutes":total_minutes,
        "times":times,
    }

    if (emp_id != []):
        times = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ctx = {
            "Employees":Employees,
            "Dates":Dates,
            "Cities":Cities,
        }
        for e in emp_id:
            Employee = Propio.objects.get(employee_id=e)
            Call_History = Propio_CallHistory.objects.filter(employee_id=Employee)
            total_calls = Propio_CallHistory.objects.filter(employee_id=Employee).count()
            total_minutes = Propio_CallHistory.objects.filter(employee_id=Employee).aggregate(Sum('interaction_length_minutes'))
            
            for c in Call_History:
                times[c.interaction_start_time.hour] += 1

            if (Date != []):
                times = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                for d in Date:
                    date_formated = datetime.strptime(d, '%b. %d, %Y').date()
                    Call_History = Propio_CallHistory.objects.filter(interaction_date=date_formated, employee_id=Employee)
                    total_calls = Propio_CallHistory.objects.filter(interaction_date=date_formated, employee_id=Employee).count()
                    total_minutes = Propio_CallHistory.objects.filter(interaction_date=date_formated, employee_id=Employee).aggregate(Sum('interaction_length_minutes'))
                    for c in Call_History:
                        times[c.interaction_start_time.hour] += 1

                    if (city != []):
                        times = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                        for c in city:
                            Call_History = Propio_CallHistory.objects.filter(employee_id__city__city=c)
                            total_calls = Propio_CallHistory.objects.filter(employee_id__city__city=c).count()
                            total_minutes = Propio_CallHistory.objects.filter(employee_id__city__city=c).aggregate(Sum('interaction_length_minutes'))
                            for c in Call_History:
                                times[c.interaction_start_time.hour] += 1
                            
                            if "data" in ctx:
                                ctx["data"] = ctx["data"].union(Call_History)
                            else:
                                ctx["data"] = Call_History
                            
                            if (total_minutes["interaction_length_minutes__sum"] == None):
                                minutes += 0
                            else:
                                minutes += total_minutes["interaction_length_minutes__sum"]
                            
                            calls += total_calls
                    else:
                        if "data" in ctx:
                            ctx["data"] = ctx["data"].union(Call_History)
                        else:
                            ctx["data"] = Call_History

                        calls += total_calls
                        if (total_minutes["interaction_length_minutes__sum"] == None):
                            minutes += 0
                        else:
                            minutes += total_minutes["interaction_length_minutes__sum"]
            else:
                calls += total_calls
                if "data" in ctx:
                    ctx["data"] = ctx["data"].union(Call_History)
                else:
                    ctx["data"] = Call_History

                if (total_minutes["interaction_length_minutes__sum"] == None):
                    minutes += 0
                else:
                    minutes += total_minutes["interaction_length_minutes__sum"]

            ctx["total_calls"] = calls
            ctx["total_minutes"] = minutes
            ctx["times"] = times

    elif (Date != []):
        times = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ctx = {
            "Employees":Employees,
            "Dates":Dates,
            "Cities":Cities,
        }
        for d in Date:
            date_formated = datetime.strptime(d, '%b. %d, %Y').date()
            Call_History = Propio_CallHistory.objects.filter(interaction_date=date_formated)
            total_calls = Propio_CallHistory.objects.filter(interaction_date=date_formated).count()
            total_minutes = Propio_CallHistory.objects.filter(interaction_date=date_formated).aggregate(Sum('interaction_length_minutes'))
            for c in Call_History:
                times[c.interaction_start_time.hour] += 1

            if (city != []):
                times = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                for c in city:
                    Call_History = Propio_CallHistory.objects.filter(employee_id__city__city=c)
                    total_calls = Propio_CallHistory.objects.filter(employee_id__city__city=c).count()
                    total_minutes = Propio_CallHistory.objects.filter(employee_id__city__city=c).aggregate(Sum('interaction_length_minutes'))
                    for c in Call_History:
                        times[c.interaction_start_time.hour] += 1
                    
                    if "data" in ctx:
                        ctx["data"] = ctx["data"].union(Call_History)
                    else:
                        ctx["data"] = Call_History
                    
                    if (total_minutes["interaction_length_minutes__sum"] == None):
                        minutes += 0
                    else:
                        minutes += total_minutes["interaction_length_minutes__sum"]
                    calls += total_calls
            else:
                if "data" in ctx:
                    ctx["data"] = ctx["data"].union(Call_History)
                else:
                    ctx["data"] = Call_History
            
                if (total_minutes["interaction_length_minutes__sum"] == None):
                    minutes += 0
                else:
                    minutes += total_minutes["interaction_length_minutes__sum"]
                calls += total_calls

        ctx["total_calls"] = calls
        ctx["total_minutes"] = minutes
        ctx["times"] = times
    
    elif (city != []):
        times = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ctx = {
            "Employees":Employees,
            "Dates":Dates,
            "Cities":Cities,
        }
        for c in city:
            Call_History = Propio_CallHistory.objects.filter(employee_id__city__city=c)
            total_calls = Propio_CallHistory.objects.filter(employee_id__city__city=c).count()
            total_minutes = Propio_CallHistory.objects.filter(employee_id__city__city=c).aggregate(Sum('interaction_length_minutes'))
            for c in Call_History:
                times[c.interaction_start_time.hour] += 1
            
            if "data" in ctx:
                ctx["data"] = ctx["data"].union(Call_History)
            else:
                ctx["data"] = Call_History
            
            if (total_minutes["interaction_length_minutes__sum"] == None):
                minutes += 0
            else:
                minutes += total_minutes["interaction_length_minutes__sum"]
            calls += total_calls

        ctx["total_calls"] = calls
        ctx["total_minutes"] = minutes
        ctx["times"] = times
            
        return render(request, 'reports/reports_propio.html', ctx)

    return render(request, 'reports/reports_propio.html', ctx)

@login_required
def reports_transperfect(request):
    return render(request, 'reports/reports_transperfect.html')

@login_required
def reports_transperfect_performance(request):
    Employees = Transperfect.objects.all()
    Dates = Transperfect_CallHistory.objects.order_by().values('date').distinct()
    Call_History = Transperfect_CallHistory.objects.all()
    Cities = City.objects.all()
    emp_id = request.GET.getlist('employee_id')
    Date = request.GET.getlist('date')
    city = request.GET.getlist('city')
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
        "Cities":Cities,
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
            "Cities":Cities,
        }
        for e in emp_id:
            Employee = Transperfect.objects.get(employee_id=e)
            Call_History = Transperfect_CallHistory.objects.filter(employee_id=Employee)

            if (Date != []):
                for d in Date:
                    date_formated = datetime.strptime(d, '%b. %d, %Y').date()
                    Call_History = Transperfect_CallHistory.objects.filter(date=date_formated, employee_id=Employee)
                    total_calls = Transperfect_CallHistory.objects.filter(date=date_formated, employee_id=Employee).count()

                    if (city != []):
                        for c in city:
                            Call_History = Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee ,date = date_formated)
                            total_calls = Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee ,date= date_formated).count()

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

            elif (city != []):
                for c in city:
                    Call_History = Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee)
                    total_calls = Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee).count()

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

    elif (Date != []):
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
            "Cities":Cities,
        }

        for d in Date:
            date_formated = datetime.strptime(d, '%b. %d, %Y').date()
            Call_History = Transperfect_CallHistory.objects.filter(date=date_formated)
            total_calls = Transperfect_CallHistory.objects.filter(date=date_formated).count()

            if (city != []):
                for c in city:
                    Call_History = Transperfect_CallHistory.objects.filter(employee_id__city__city = c, date = date_formated)
                    total_calls = Transperfect_CallHistory.objects.filter(employee_id__city__city = c, date= date_formated).count()

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

    elif (city != []):
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
            "Cities":Cities,
        }

        for c in city:
            Call_History = Transperfect_CallHistory.objects.filter(employee_id__city__city = c)
            total_calls = Transperfect_CallHistory.objects.filter(employee_id__city__city = c).count()

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
            
        ctx["total_calls"]=calls
        ctx["eof_minutes"]=round(eof_minutes,2)
        ctx["available_minutes"]=round(available_minutes,2)
        ctx["talk_minutes"]=round(talk_minutes,2)
        ctx["acw_minutes"]=round(acw_minutes,2)
        ctx["ring_through_minutes"]=round(ring_through_minutes,2)
        ctx["break_minutes"]=round(break_minutes,2)
        ctx["schedule_call_minutes"]=round(schedule_call_minutes,2)
        ctx["meeting_minutes"]=round(meeting_minutes,2)
        ctx["lunch_minutes"]=round(lunch_minutes,2)

        return render(request, 'reports/reports_transperfect_performance.html', ctx)

    return render(request, 'reports/reports_transperfect_performance.html', ctx)

@login_required
def reports_transperfect_production(request):
    Employees = Transperfect.objects.all()
    Dates = Production_Transperfect_CallHistory.objects.order_by().values('date').distinct()
    Languages = Production_Transperfect_CallHistory.objects.order_by().values('language').distinct()
    Call_History = Production_Transperfect_CallHistory.objects.all()
    Cities = City.objects.all()
    emp_id = request.GET.getlist('employee_id')
    Date = request.GET.getlist('date')
    city = request.GET.getlist('city')
    language = request.GET.getlist('language')

    if (Production_Transperfect_CallHistory.objects.aggregate(Sum('minutes'))['minutes__sum'] != None):
        minutes = round(next(iter(Production_Transperfect_CallHistory.objects.aggregate(Sum('minutes')).values())),2)
    else:
        minutes = 0

    if (Production_Transperfect_CallHistory.objects.aggregate(Sum('adjusted_minutes'))['adjusted_minutes__sum'] != None):
        adjust_min = round(next(iter(Production_Transperfect_CallHistory.objects.aggregate(Sum('adjusted_minutes')).values())),2)
    else:
        adjust_min = 0
    total_calls = Production_Transperfect_CallHistory.objects.all().count()
    times = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for c in Call_History:
        times[c.interaction_start_time.hour] += 1

    language_minutes = {}
    for l in Languages:
        for i in l.values():
            language_minutes["{0}".format(i)] = 0

    for c in Call_History:
        for l in Languages:
            for i in l.values():
                if (c.language == i):
                    language_minutes["{0}".format(i)] += c.adjusted_minutes

    ctx = {
        "Employees":Employees,
        "Dates":Dates,
        "Languages":Languages,
        "Cities":Cities,
        "data":Call_History,
        "total_calls":total_calls,
        "minutes":minutes,
        "adjust_min":adjust_min,
        "times":times,
        "language_minutes":language_minutes
    }

    if (emp_id != []):
        times = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        minutes = 0
        adjust_min = 0
        calls = 0
        language_minutes = {}
        ctx = {
            "Employees":Employees,
            "Dates":Dates,
            "Languages":Languages,
            "Cities":Cities,
        }

        for e in emp_id:
            Employee = Transperfect.objects.get(employee_id=e)
            Call_History = Production_Transperfect_CallHistory.objects.filter(employee_id=Employee)
            if ("{0}".format(c.language)) not in language_minutes.keys():
                for c in Call_History:
                    language_minutes["{0}".format(c.language)] = 0

            if (Date != []):
                for d in Date:
                    date_formated = datetime.strptime(d, '%b. %d, %Y').date()
                    Call_History = Production_Transperfect_CallHistory.objects.filter(date=date_formated, employee_id=Employee)
                    total_calls = Production_Transperfect_CallHistory.objects.filter(date=date_formated, employee_id=Employee).count()
                    if (Production_Transperfect_CallHistory.objects.filter(date=date_formated, employee_id=Employee)):
                        minutes += next(iter(Production_Transperfect_CallHistory.objects.filter(date=date_formated, employee_id=Employee).aggregate(Sum('minutes')).values()))
                    else:
                        minutes += 0
                    
                    if(Production_Transperfect_CallHistory.objects.filter(date=date_formated, employee_id=Employee)):
                        adjust_min += next(iter(Production_Transperfect_CallHistory.objects.filter(date=date_formated, employee_id=Employee).aggregate(Sum('adjusted_minutes')).values()))
                    else:
                        minutes += 0
                    
                    if (city != []):
                        for c in city:
                            Call_History = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee ,date = date_formated)
                            total_calls = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee ,date= date_formated).count()
                            
                            if (language != []):
                                for l in language:
                                    Call_History = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee ,date = date_formated,language=l)
                                    total_calls = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee ,date= date_formated,language=l).count()
                                    
                                    if (Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee ,date= date_formated, language=l)):
                                        minutes += next(iter(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee ,date= date_formated, language=l).aggregate(Sum('minutes')).values()))
                                    else:
                                        minutes += 0
                                    
                                    if(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee ,date= date_formated, language=l)):
                                        adjust_min += next(iter(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee ,date= date_formated, language=l).aggregate(Sum('adjusted_minutes')).values()))
                                    else:
                                        minutes += 0
                                    
                                    if "data" in ctx:
                                        ctx["data"] = ctx["data"].union(Call_History)
                                    else:
                                        ctx["data"] = Call_History
                                    
                                    for c in Call_History:
                                        times[c.interaction_start_time.hour] += 1

                                    calls += total_calls

                                    for c in Call_History:
                                        for l in Languages:
                                            for i in l.values():
                                                if (c.language == i):
                                                    language_minutes["{0}".format(i)] += c.adjusted_minutes

                            else:
                                if (Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee ,date= date_formated)):
                                    minutes += next(iter(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee ,date= date_formated).aggregate(Sum('minutes')).values()))
                                else:
                                    minutes += 0
                                
                                if(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee ,date= date_formated)):
                                    adjust_min += next(iter(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee ,date= date_formated).aggregate(Sum('adjusted_minutes')).values()))
                                else:
                                    minutes += 0
                                
                                if "data" in ctx:
                                    ctx["data"] = ctx["data"].union(Call_History)
                                else:
                                    ctx["data"] = Call_History
                                
                                for c in Call_History:
                                    times[c.interaction_start_time.hour] += 1

                                calls += total_calls

                                for c in Call_History:
                                    for l in Languages:
                                        for i in l.values():
                                            if (c.language == i):
                                                language_minutes["{0}".format(i)] += c.adjusted_minutes

                    else:
                        
                        for c in Call_History:
                            times[c.interaction_start_time.hour] += 1

                        if "data" in ctx:
                            ctx["data"] = ctx["data"].union(Call_History)
                        else:
                            ctx["data"] = Call_History
                        
                        for c in Call_History:
                            for l in Languages:
                                for i in l.values():
                                    if (c.language == i):
                                        language_minutes["{0}".format(i)] += c.adjusted_minutes
                                        print(language_minutes)

                        calls += total_calls

            elif (city != []):
                for c in city:
                    Call_History = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee)
                    total_calls = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee).count()

                    if(language!=[]):

                        for l in language:
                            Call_History = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee,language=l)
                            total_calls = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee,language=l).count()

                            if (Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee, language=l)):
                                minutes += next(iter(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee, language=l).aggregate(Sum('minutes')).values()))
                            else:
                                minutes += 0
                            
                            if(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee, language=l)):
                                adjust_min += next(iter(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee, language=l).aggregate(Sum('adjusted_minutes')).values()))
                            else:
                                minutes += 0

                            if "data" in ctx:
                                ctx["data"] = ctx["data"].union(Call_History)
                            else:
                                ctx["data"] = Call_History

                            for c in Call_History:
                                times[c.interaction_start_time.hour] += 1
                            
                            for c in Call_History:
                                for l in Languages:
                                    for i in l.values():
                                        if (c.language == i):
                                            language_minutes["{0}".format(i)] += c.adjusted_minutes

                            calls += total_calls
                    else:
                        if (Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee)):
                            minutes += next(iter(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee).aggregate(Sum('minutes')).values()))
                        else:
                            minutes += 0
                        
                        if(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee)):
                            adjust_min += next(iter(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee).aggregate(Sum('adjusted_minutes')).values()))
                        else:
                            minutes += 0

                        if "data" in ctx:
                            ctx["data"] = ctx["data"].union(Call_History)
                        else:
                            ctx["data"] = Call_History

                        for c in Call_History:
                            times[c.interaction_start_time.hour] += 1

                        for c in Call_History:
                            for l in Languages:
                                for i in l.values():
                                    if (c.language == i):
                                        language_minutes["{0}".format(i)] += c.adjusted_minutes

                        calls += total_calls
            
            elif (language != []):
                for l in language:
                    Call_History = Production_Transperfect_CallHistory.objects.filter(language=l, employee_id=Employee)
                    total_calls = Production_Transperfect_CallHistory.objects.filter(language=l, employee_id=Employee).count()

                    if (Production_Transperfect_CallHistory.objects.filter(language=l, employee_id=Employee)):
                        minutes += next(iter(Production_Transperfect_CallHistory.objects.filter(language=l, employee_id=Employee).aggregate(Sum('minutes')).values()))
                    else:
                        minutes += 0
                    
                    if(Production_Transperfect_CallHistory.objects.filter(language=l, employee_id=Employee)):
                        adjust_min += next(iter(Production_Transperfect_CallHistory.objects.filter(language=l, employee_id=Employee).aggregate(Sum('adjusted_minutes')).values()))
                    else:
                        minutes += 0

                    if "data" in ctx:
                        ctx["data"] = ctx["data"].union(Call_History)
                    else:
                        ctx["data"] = Call_History

                    for c in Call_History:
                        times[c.interaction_start_time.hour] += 1

                    calls += total_calls

                    for c in Call_History:
                        for l in Languages:
                            for i in l.values():
                                if (c.language == i):
                                    language_minutes["{0}".format(i)] += c.adjusted_minutes

            else:
                total_calls = Production_Transperfect_CallHistory.objects.filter(employee_id=Employee).count()
                if (Production_Transperfect_CallHistory.objects.filter(employee_id=Employee)):
                    minutes += next(iter(Production_Transperfect_CallHistory.objects.filter(employee_id=Employee).aggregate(Sum('minutes')).values()))
                else:
                    minutes += 0
                
                if(Production_Transperfect_CallHistory.objects.filter(employee_id=Employee)):
                    adjust_min += next(iter(Production_Transperfect_CallHistory.objects.filter(employee_id=Employee).aggregate(Sum('adjusted_minutes')).values()))
                else:
                    minutes += 0

                for c in Call_History:
                    times[c.interaction_start_time.hour] += 1

                calls += total_calls
                if "data" in ctx:
                    ctx["data"] = ctx["data"].union(Call_History)
                else:
                    ctx["data"] = Call_History

                for c in Call_History:
                    for l in Languages:
                        for i in l.values():
                            if (c.language == i):
                                language_minutes["{0}".format(i)] += c.adjusted_minutes
            
            ctx["total_calls"] = calls
            ctx["minutes"] = round(minutes,2)
            ctx["adjust_min"] = round(adjust_min,2)
            ctx["times"] = times
            ctx["language_minutes"] = language_minutes

    elif (Date != []):
        times = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        minutes = 0
        adjust_min = 0
        calls = 0
        language_minutes = {}
        ctx = {
            "Employees":Employees,
            "Dates":Dates,
            "Languages":Languages,
            "Cities":Cities,
        }

        for d in Date:
            date_formated = datetime.strptime(d, '%b. %d, %Y').date()
            Call_History = Production_Transperfect_CallHistory.objects.filter(date=date_formated)
            total_calls = Production_Transperfect_CallHistory.objects.filter(date=date_formated).count()

            if ("{0}".format(c.language)) not in language_minutes.keys():
                for c in Call_History:
                    language_minutes["{0}".format(c.language)] = 0

            if (city != []):
                for c in city:
                    Call_History = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, date = date_formated)
                    total_calls = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, date= date_formated).count()
                    
                    if (language != []):
                        for l in language:
                            Call_History = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, date = date_formated, language=l)
                            total_calls = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, date= date_formated, language=l).count()
                            if (Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, date = date_formated, language=l)):
                                minutes += next(iter(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, date = date_formated, language=l).aggregate(Sum('minutes')).values()))
                            else:
                                minutes += 0
                            
                            if(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, date = date_formated, language=l)):
                                adjust_min += next(iter(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, date = date_formated, language=l).aggregate(Sum('adjusted_minutes')).values()))
                            else:
                                minutes += 0
                            
                            if "data" in ctx:
                                ctx["data"] = ctx["data"].union(Call_History)
                            else:
                                ctx["data"] = Call_History

                            for c in Call_History:
                                times[c.interaction_start_time.hour] += 1

                            calls += total_calls

                            for c in Call_History:
                                for l in Languages:
                                    for i in l.values():
                                        if (c.language == i):
                                            language_minutes["{0}".format(i)] += c.adjusted_minutes

                    else:
                        if (Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, date = date_formated)):
                            minutes += next(iter(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, date = date_formated).aggregate(Sum('minutes')).values()))
                        else:
                            minutes += 0
                        
                        if(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, date = date_formated)):
                            adjust_min += next(iter(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, date = date_formated).aggregate(Sum('adjusted_minutes')).values()))
                        else:
                            minutes += 0
                        
                        if "data" in ctx:
                            ctx["data"] = ctx["data"].union(Call_History)
                        else:
                            ctx["data"] = Call_History

                        for c in Call_History:
                            times[c.interaction_start_time.hour] += 1

                        calls += total_calls

                        for c in Call_History:
                            for l in Languages:
                                for i in l.values():
                                    if (c.language == i):
                                        language_minutes["{0}".format(i)] += c.adjusted_minutes

            elif (language != []):
                for l in language:
                    Call_History = Production_Transperfect_CallHistory.objects.filter(language=l, date = date_formated)
                    total_calls = Production_Transperfect_CallHistory.objects.filter(language=l, date= date_formated).count()
                    
                    if (Production_Transperfect_CallHistory.objects.filter(language=l, date = date_formated)):
                        minutes += next(iter(Production_Transperfect_CallHistory.objects.filter(language=l, date = date_formated).aggregate(Sum('minutes')).values()))
                    else:
                        minutes += 0
                        
                    if(Production_Transperfect_CallHistory.objects.filter(language=l, date = date_formated)):
                        adjust_min += next(iter(Production_Transperfect_CallHistory.objects.filter(language=l, date = date_formated).aggregate(Sum('adjusted_minutes')).values()))
                    else:
                        minutes += 0
        
                    if "data" in ctx:
                        ctx["data"] = ctx["data"].union(Call_History)
                    else:
                        ctx["data"] = Call_History

                    for c in Call_History:
                        times[c.interaction_start_time.hour] += 1

                    calls += total_calls

                    for c in Call_History:
                        for l in Languages:
                            for i in l.values():
                                if (c.language == i):
                                    language_minutes["{0}".format(i)] += c.adjusted_minutes

            else:
                total_calls = Production_Transperfect_CallHistory.objects.filter(date=date_formated).count()
                
                if (Production_Transperfect_CallHistory.objects.filter(date=date_formated)):
                    minutes += next(iter(Production_Transperfect_CallHistory.objects.filter(date=date_formated).aggregate(Sum('minutes')).values()))
                else:
                    minutes += 0
                    
                if(Production_Transperfect_CallHistory.objects.filter(date=date_formated)):
                    adjust_min += next(iter(Production_Transperfect_CallHistory.objects.filter(date=date_formated).aggregate(Sum('adjusted_minutes')).values()))
                else:
                    minutes += 0
                
                if "data" in ctx:
                    ctx["data"] = ctx["data"].union(Call_History)
                else:
                    ctx["data"] = Call_History

                for c in Call_History:
                    times[c.interaction_start_time.hour] += 1

                calls += total_calls

                for c in Call_History:
                    for l in Languages:
                        for i in l.values():
                            if (c.language == i):
                                language_minutes["{0}".format(i)] += c.adjusted_minutes
            
            ctx["total_calls"] = calls
            ctx["minutes"] = round(minutes,2)
            ctx["adjust_min"] = round(adjust_min,2)
            ctx["times"] = times
            ctx["language_minutes"] = language_minutes

    elif (city != []):
        times = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        minutes = 0
        adjust_min = 0
        calls = 0
        language_minutes = {}
        ctx = {
            "Employees":Employees,
            "Dates":Dates,
            "Languages":Languages,
            "Cities":Cities,
        }

        for c in city:
            Call_History = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c)
            total_calls = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c).count()

            if ("{0}".format(c.language)) not in language_minutes.keys():
                for c in Call_History:
                    language_minutes["{0}".format(c.language)] = 0

            if(language!=[]):
                    Call_History = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c,language=l)
                    total_calls = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c,language=l).count()
                    
                    if (Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c,language=l)):
                        minutes += next(iter(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c,language=l).aggregate(Sum('minutes')).values()))
                    else:
                        minutes += 0
                        
                    if(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c,language=l)):
                        adjust_min += next(iter(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c,language=l).aggregate(Sum('adjusted_minutes')).values()))
                    else:
                        minutes += 0
                    
                    if "data" in ctx:
                        ctx["data"] = ctx["data"].union(Call_History)
                    else:
                        ctx["data"] = Call_History

                    for c in Call_History:
                        times[c.interaction_start_time.hour] += 1

                    calls += total_calls

                    for c in Call_History:
                        for l in Languages:
                            for i in l.values():
                                if (c.language == i):
                                    language_minutes["{0}".format(i)] += c.adjusted_minutes

            else:
                if (Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c)):
                    minutes += next(iter(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c).aggregate(Sum('minutes')).values()))
                else:
                    minutes += 0
                    
                if(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c)):
                    adjust_min += next(iter(Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c).aggregate(Sum('adjusted_minutes')).values()))
                else:
                    minutes += 0
                
                if "data" in ctx:
                    ctx["data"] = ctx["data"].union(Call_History)
                else:
                    ctx["data"] = Call_History

                for c in Call_History:
                    times[c.interaction_start_time.hour] += 1

                calls += total_calls

                for c in Call_History:
                    for l in Languages:
                        for i in l.values():
                            if (c.language == i):
                                language_minutes["{0}".format(i)] += c.adjusted_minutes
            
        ctx["total_calls"] = calls
        ctx["minutes"] = round(minutes,2)
        ctx["adjust_min"] = round(adjust_min,2)
        ctx["times"] = times
        ctx["language_minutes"] = language_minutes

        return render(request, 'reports/reports_transperfect_production.html', ctx)

    elif (language != []):
        times = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        minutes = 0
        adjust_min = 0
        calls = 0
        language_minutes = {}
        ctx = {
            "Employees":Employees,
            "Dates":Dates,
            "Languages":Languages,
            "Cities":Cities,
        }

        for l in language:
            Call_History = Production_Transperfect_CallHistory.objects.filter(language = l)
            total_calls = Production_Transperfect_CallHistory.objects.filter(language = l).count()

            if ("{0}".format(c.language)) not in language_minutes.keys():
                for c in Call_History:
                    language_minutes["{0}".format(c.language)] = 0
            
            if (Production_Transperfect_CallHistory.objects.filter(language = l)):
                minutes += next(iter(Production_Transperfect_CallHistory.objects.filter(language = l).aggregate(Sum('minutes')).values()))
            else:
                minutes += 0
                
            if(Production_Transperfect_CallHistory.objects.filter(language = l)):
                adjust_min += next(iter(Production_Transperfect_CallHistory.objects.filter(language = l).aggregate(Sum('adjusted_minutes')).values()))
            else:
                minutes += 0
            
            if "data" in ctx:
                ctx["data"] = ctx["data"].union(Call_History)
            else:
                ctx["data"] = Call_History

            for c in Call_History:
                times[c.interaction_start_time.hour] += 1

            calls += total_calls

            for c in Call_History:
                    for l in Languages:
                        for i in l.values():
                            if (c.language == i):
                                language_minutes["{0}".format(i)] += c.adjusted_minutes
            
        ctx["total_calls"] = calls
        ctx["minutes"] = round(minutes,2)
        ctx["adjust_min"] = round(adjust_min,2)
        ctx["times"] = times
        ctx["language_minutes"] = language_minutes

        return render(request, 'reports/reports_transperfect_production.html', ctx)

    return render(request, 'reports/reports_transperfect_production.html', ctx)

@login_required
def employees_transperfect_performance(request):
    date_call_history = request.POST.get('date')
    timestamp = datetime.now()
    today = date.today()
    week = today - timedelta(days=7)
    
    ctx = {
        "today":today.strftime("%Y-%m-%d"),
        "week":week.strftime("%Y-%m-%d"),
    }

    if (request.method == "POST"):
        file = request.FILES['call-history']
        df=pd.read_excel(file, skiprows=2)
        print(df)
        try:
            df.columns=["Unnamed: 0","Unnamed: 1","unavailable - end of shift","available", "Talk Time", "unavailable - acw","unavailable - ring-through","unavailable - break","unavailable - scheduled call","unavailable - meeting","unavailable - lunch"]
        except:
            messages.error(request, 'Some of the data seems to not match with the correct format.')
            return render(request, 'reports/performance_transperfect.html',ctx)
        for x in range(len(df["Unnamed: 1"])):
            if isinstance(df["Unnamed: 1"][x],str):
                try:
                    datetime.strptime(df["unavailable - end of shift"][x],'%H:%M:%S')
                    datetime.strptime(df["available"][x],'%H:%M:%S')
                    datetime.strptime(df["Talk Time"][x],'%H:%M:%S')
                    datetime.strptime(df["unavailable - acw"][x],'%H:%M:%S')
                    datetime.strptime(df["unavailable - ring-through"][x],'%H:%M:%S')
                    datetime.strptime(df["unavailable - break"][x],'%H:%M:%S')
                    datetime.strptime(df["unavailable - scheduled call"][x],'%H:%M:%S')
                    datetime.strptime(df["unavailable - meeting"][x],'%H:%M:%S')
                    datetime.strptime(df["unavailable - lunch"][x],'%H:%M:%S')
                except:
                    messages.error(request, 'Some of the data seems to not match with the correct format.')
                    return render(request, 'reports/production_transperfect.html')
        for x in range(len(df["Unnamed: 1"])):
            if isinstance(df["Unnamed: 1"][x], str):
                try:
                    employee = Transperfect.objects.get(transperfect_id=df["Unnamed: 1"][x])
                except:
                    messages.error(request, 'Some of the employees are not in the database.')
                    return render(request, 'reports/production_transperfect.html')
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
                    created = timestamp,
                )
                calls.save()
        messages.success(request, 'The data has been uploaded.')
        return render(request, 'reports/performance_transperfect.html', ctx)
    return render(request, 'reports/performance_transperfect.html', ctx)

@login_required
def employees_transperfect_production(request):
    timestamp = datetime.now()
    if (request.method == "POST"):
        adjust_min = request.POST.get('adjust')
        file = request.FILES['call-history']
        df=pd.read_excel(file)
        try:
            df.columns=["Employee_ID","Full Name","Language", "StartDate", "EndDate","Real Minutes","SpeedOfAnswer"]
        except:
            messages.error(request, 'Some of the data seems to not match with the correct format.')
            return render(request, 'reports/production_transperfect.html')
        for x in range(len(df["Employee_ID"])):
            if not(isinstance(df["Employee_ID"][x],str) and isinstance(df["Full Name"][x],str) and isinstance(df["Language"][x],str) and isinstance(df["StartDate"][x],datetime) and isinstance(df["EndDate"][x],datetime) and isinstance(df["Real Minutes"][x],np.floating) and isinstance(df["SpeedOfAnswer"][x],np.integer)):
                messages.error(request, 'Some of the data seems to not match with the correct format.')
                return render(request, 'reports/production_transperfect.html')
        for x in range(len(df["Employee_ID"])):
            if isinstance(df["Employee_ID"][x], str):
                try:
                    employee = Transperfect.objects.get(transperfect_id=df["Employee_ID"][x])
                except:
                    messages.error(request, 'Some of the employees are not in the database.')
                    return render(request, 'reports/production_transperfect.html')
                interaction_date = df["StartDate"][x].date()
                interaction_start_time = df["StartDate"][x]
                interaction_end_time = df["EndDate"][x]
                language = df["Language"][x]
                minutes = df["Real Minutes"][x]
                speed_answer = df["SpeedOfAnswer"][x]
                if ((df["Real Minutes"][x] - float(adjust_min)) < 2):
                    adjusted_minutes = df["Real Minutes"][x]
                else:
                    adjusted_minutes = df["Real Minutes"][x] - float(adjust_min)
                
                calls = Production_Transperfect_CallHistory(
                    employee_id=employee,
                    date=interaction_date,
                    interaction_start_time= interaction_start_time,
                    interaction_end_time=interaction_end_time,
                    language=language,
                    minutes=minutes,
                    speed_answer=speed_answer,
                    adjusted_minutes=adjusted_minutes,
                    created = timestamp,
                )
                calls.save()
        messages.success(request, 'The data has been uploaded.')
        return render(request, 'reports/production_transperfect.html')
    return render(request, 'reports/production_transperfect.html')

@login_required
def employees_propio(request):
    Employees = Propio.objects.all()
    timestamp = datetime.now()
    if (request.method == "POST"):
        emp_id = request.POST.get('employee')
        employee = Propio.objects.get(employee_id=emp_id)
        file = request.FILES['call-history']
        df=pd.read_excel(file)
        try:
            df.columns=["LABEL-1","LABEL-2","LABEL-3", "LABEL-4", "LABEL-5","LABEL-6","LABEL-7"]
        except:
            messages.error(request, 'Some of the data seems to not match with the correct format.')
            ctx = {
                "Employees": Employees,
            }
            return render(request, 'reports/employees_propio.html', ctx)
       
        for x in range(len(df["LABEL-1"])):
            if not(isinstance(df["LABEL-2"][x],str) and isinstance(df["LABEL-3"][x],datetime) and isinstance(df["LABEL-4"][x],time) and isinstance(df["LABEL-5"][x],time)):
                messages.error(request, 'Some of the data seems to not match with the correct format.')
                ctx = {
                    "Employees": Employees,
                }
                return render(request, 'reports/employees_propio.html', ctx)
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
                
            datetime_formated = datetime.strptime('{0} {1}'.format((df["LABEL-3"][x]).date(),df["LABEL-4"][x]), '%Y-%m-%d %H:%M:%S')
            calls = Propio_CallHistory(
                employee_id = employee,
                interaction_date  = (df["LABEL-3"][x]),
                interaction_start_time = datetime_formated,
                interaction_length = lenght,
                interaction_length_minutes = ((df["LABEL-5"][x].hour * 60) + df["LABEL-5"][x].minute),
                created = timestamp,
            )
            calls.save()
        messages.success(request, 'The data has been uploaded.')
        ctx = {
            "Employees": Employees,
        }
        return render(request, 'reports/employees_propio.html', ctx)


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

        try:
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
        except:
            messages.error(request, "It seems that either the 'Employee ID' or the 'Propio ID' were already in use.")
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
        messages.success(request, "The employee was successfully added.")
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

