from datetime import datetime, date, timedelta, time
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from .models import *
import pandas as pd
import numpy as np
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def accounts(request):
    # Crear una nueva sesion, la sesion cumplira el proposito de contar los minutos para cerrar la sesion despues de inactividad
    request.session['name'] = 'cookie'

    return render (request, 'reports/accounts_upload.html')

@login_required
def transperfect(request):
    # Refrescar la sesion para que el cronometro interno vuelva a contar los 20 minutos de inactividad desde 0
    session = request.session['name']

    return render (request, 'reports/transperfect_upload.html')

@login_required
def reports(request):
    return render(request, 'reports/accounts_reports.html')

@login_required
def reports_propio(request):
    # Cargar todos los empleados de Propio
    Employees = Propio.objects.all()
    # Cargar las diferentes fechas guardas
    Dates = Propio_CallHistory.objects.order_by().values('interaction_date').distinct()
    # Cargar todas las ciudades
    Cities = City.objects.all()
    # Cargar el historial de llamadas de Propio
    Call_History = Propio_CallHistory.objects.all()

    # Informacion obtenida de la vista reportes Propio para el filtrado de los datos
    # Obtener los empleados seleccionados
    emp_id = request.GET.getlist('employee_id')
    # Obtener las fechas seleccionadas
    Date = request.GET.getlist('date')
    # Obtener las ciudades seleccionadas
    city = request.GET.getlist('city')

    # Variable que contiene la cantidad de minutos totales dependiendo del filtro
    minutes = 0
    # Variable que contiene la cantidad de minutos totales de todos los datos
    total_minutes = Propio_CallHistory.objects.aggregate(Sum('interaction_length_minutes'))
    # Variable que contiene el numero de llamadas dependiendo del filtro
    calls = 0
    # Variable que contiene el numero de llamadas totales de todos los datos
    total_calls = Propio_CallHistory.objects.all().count()
    # Lista de las 24 horas del día
    times = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    # Ciclando todos los datos y contando cuantas veces una llamada ocurrio a cierta hora del dia
    for c in Call_History:
        times[c.interaction_start_time.hour] += 1

    # Contexto que sera enviado a la vista
    ctx = {
        "Employees":Employees,
        "Dates":Dates,
        "Cities":Cities,
        "data":Call_History,
        "total_calls":total_calls,
        "total_minutes":total_minutes,
        "times":times,
    }

    # Si se escoge como filtro uno o mas empleados
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
            
            # Si se escoge como filtro una o mas fechas
            if (Date != []):
                times = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                for d in Date:
                    date_formated = datetime.strptime(d, '%b. %d, %Y').date()
                    Call_History = Propio_CallHistory.objects.filter(interaction_date=date_formated, employee_id=Employee)
                    total_calls = Propio_CallHistory.objects.filter(interaction_date=date_formated, employee_id=Employee).count()
                    total_minutes = Propio_CallHistory.objects.filter(interaction_date=date_formated, employee_id=Employee).aggregate(Sum('interaction_length_minutes'))
                    for c in Call_History:
                        times[c.interaction_start_time.hour] += 1

                    # Si se escoge como filtro una o mas ciudades
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
    # Si se escoge como filtro una o mas fechas
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

            # Si se escoge como filtro una o mas ciudades
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
    # i se escoge como filtro una o mas ciudades
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
    # Todos los empleados de transperfect guardadas en la base de datos
    Employees = Transperfect.objects.all()
    # Las diferentes fechas guardadas en el historial de llamadas de Transperfect desempeño
    Dates = Transperfect_CallHistory.objects.order_by().values('date').distinct()
    # Todos las llamadas guardadas en el historial de Transperfect desempeño
    Call_History = Transperfect_CallHistory.objects.all()
    # Todas las ciudades registradas en la base de datos
    Cities = City.objects.all()
    
    # Informacion obtenida de la vista reportes Transperfect desempeño para el filtrado de los datos
    # Obtener los empleados seleccionados
    emp_id = request.GET.getlist('employee_id')
    # Obtener las fechas seleccionadas
    Date = request.GET.getlist('date')
    # Obtener las ciudades seleccionadas
    city = request.GET.getlist('city')

    # Variable que contiene la cantidad de minutos fuera de turno dependiendo del filtro
    eof_minutes = 0
    # Variable que contiene la cantidad de minutos conectado dependiendo del filtro
    available_minutes = 0
    # Variable que contiene la cantidad de minutos en llamada dependiendo del filtro
    talk_minutes = 0
    # Variable que contiene la cantidad de minutos de reposo entre llamadas dependiendo del filtro
    acw_minutes = 0
    # Variable que contiene la cantidad de minutos de llamadas perdidas dependiendo del filtro
    ring_through_minutes = 0
    # Variable que contiene la cantidad de minutos de los recesos dependiendo del filtro
    break_minutes = 0
    # Variable que contiene la cantidad de minutos  dependiendo del filtro
    schedule_call_minutes = 0
    # Variable que contiene la cantidad de minutos en una reunion dependiendo del filtro
    meeting_minutes = 0
    # Variable que contiene la cantidad de minutos de almuerzo dependiendo del filtro
    lunch_minutes = 0
    # Variable que contiene la cantidad de llamadas en el historial dependiendo del filtro
    calls = 0
    # Variable que contiene la cantidad total de minutos en el historia de Transperfect performance
    total_calls = Transperfect_CallHistory.objects.all().count()

    # Por cada entrada en el historial suma los diferentes tipos de minutos a su repectiva variable
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
    
    # Contexto que sera enviado devuelta a la vista
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

    # Si se escoge una o mas empleados para el filtro
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
            
            # Si se escoge una o mas fechas para el filtro
            if (Date != []):
                for d in Date:
                    date_formated = datetime.strptime(d, '%b. %d, %Y').date()
                    Call_History = Transperfect_CallHistory.objects.filter(date=date_formated, employee_id=Employee)
                    total_calls = Transperfect_CallHistory.objects.filter(date=date_formated, employee_id=Employee).count()

                    # Si se escoge uno o mas ciudades para el filtro
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

            # Si se escoge una o mas ciudades para el filtro
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
    # Si se escoge una o mas fechas para el filtro
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

            # Si se escoge una o mas ciudades para el filtro
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
    # Si se escoge una o mas ciudades para el filtro
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
    # Todos los empleados de transperfect guardadas en la base de datos
    Employees = Transperfect.objects.all()
    # Las diferentes fechas guardadas en el historial de llamadas de Transperfect producción
    Dates = Production_Transperfect_CallHistory.objects.order_by().values('date').distinct()
    # Todos los idiomas en el historial de Transperfect producción
    Languages = Production_Transperfect_CallHistory.objects.order_by().values('language').distinct()
    # Todos las llamadas guardadas en el historial de Transperfect producción
    Call_History = Production_Transperfect_CallHistory.objects.all()
    # Todas las ciudades registradas en la base de datos
    Cities = City.objects.all()
    
    # Informacion obtenida de la vista reportes Transperfect-performance para el filtrado de los datos
    # Obtener los empleados seleccionados
    emp_id = request.GET.getlist('employee_id')
    # Obtener las fechas seleccionadas
    Date = request.GET.getlist('date')
    # Obtener las ciudades seleccionadas
    city = request.GET.getlist('city')
    # Obtener los idiomas seleccionados
    language = request.GET.getlist('language')

    # Si hay llamadas en el historial de Transperfect producción, redondear la suma total de minutos a 2 decimales despues del punto
    if (Production_Transperfect_CallHistory.objects.aggregate(Sum('minutes'))['minutes__sum'] != None):
        minutes = round(next(iter(Production_Transperfect_CallHistory.objects.aggregate(Sum('minutes')).values())),2)
    else:
        minutes = 0

    # Si hay llamadas en el historial de Transperfect producción, redondear la suma total de los minutos ajustados a 2 decimales despues del punto
    if (Production_Transperfect_CallHistory.objects.aggregate(Sum('adjusted_minutes'))['adjusted_minutes__sum'] != None):
        adjust_min = round(next(iter(Production_Transperfect_CallHistory.objects.aggregate(Sum('adjusted_minutes')).values())),2)
    else:
        adjust_min = 0
    
    # Variable que contiene el total de llamadas registradas en el historial de Transperfect producción
    total_calls = Production_Transperfect_CallHistory.objects.all().count()
    # Lista de las 24 horas del día
    times = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    # Ciclando todos los datos y contando cuantas veces una llamada ocurrio a cierta hora del día
    for c in Call_History:
        times[c.interaction_start_time.hour] += 1

    # Diccionario de los diferentes idiomas
    language_minutes = {}
    # Agregar cada idioma al disccionario
    for l in Languages:
        for i in l.values():
            language_minutes["{0}".format(i)] = 0

    # Calcular el total de minutos por idioma entre todas las entradas guardadas en el historial de llamadas de Transperfect producción
    for c in Call_History:
        for l in Languages:
            for i in l.values():
                if (c.language == i):
                    language_minutes["{0}".format(i)] += c.minutes

    # Contexto que sera enviado a la vista
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

    # Si se escoge una o mas empleados para el filtro
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
            # Si se escoge una o mas fechas para el filtro
            if (Date != []):
                for d in Date:
                    date_formated = datetime.strptime(d, '%B %d, %Y').date()
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
                    # Si se escoge una o mas ciudades para el filtro
                    if (city != []):
                        for c in city:
                            Call_History = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee ,date = date_formated)
                            total_calls = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee ,date= date_formated).count()
                            
                            # Si se escoge uno o mas idiomas para el filtro
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
                                                    language_minutes["{0}".format(i)] += c.minutes

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
                                        language_minutes["{0}".format(i)] += c.minutes

                        calls += total_calls
            # Si se escoge una o mas ciudades para el filtro
            elif (city != []):
                for c in city:
                    Call_History = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee)
                    total_calls = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, employee_id=Employee).count()
                    # Si se escoge uno o mas idiomas para el filtro
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
                                            language_minutes["{0}".format(i)] += c.minutes

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
                                        language_minutes["{0}".format(i)] += c.minutes

                        calls += total_calls
            # Si se escoge uno o mas idiomas para el filtro
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
                                    language_minutes["{0}".format(i)] += c.minutes

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
                                language_minutes["{0}".format(i)] += c.minutes
            
            ctx["total_calls"] = calls
            ctx["minutes"] = round(minutes,2)
            ctx["adjust_min"] = round(adjust_min,2)
            ctx["times"] = times
            ctx["language_minutes"] = language_minutes
    # Si se escoge una o mas fechas para el filtro
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
            date_formated = datetime.strptime(d, '%B %d, %Y').date()
            Call_History = Production_Transperfect_CallHistory.objects.filter(date=date_formated)
            total_calls = Production_Transperfect_CallHistory.objects.filter(date=date_formated).count()

            if ("{0}".format(c.language)) not in language_minutes.keys():
                for c in Call_History:
                    language_minutes["{0}".format(c.language)] = 0
            # Si se escoge una o mas ciudades para el filtro
            if (city != []):
                for c in city:
                    Call_History = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, date = date_formated)
                    total_calls = Production_Transperfect_CallHistory.objects.filter(employee_id__city__city = c, date= date_formated).count()
                    
                    # Si se escoge uno o mas idiomas para el filtro
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
                                            language_minutes["{0}".format(i)] += c.minutes

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
            # Si se escoge uno o mas idiomas para el filtro
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
                                    language_minutes["{0}".format(i)] += c.minutes

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
                                language_minutes["{0}".format(i)] += c.minutes
            
            ctx["total_calls"] = calls
            ctx["minutes"] = round(minutes,2)
            ctx["adjust_min"] = round(adjust_min,2)
            ctx["times"] = times
            ctx["language_minutes"] = language_minutes
    # Si se escoge una o mas ciudades para el filtro
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

            # Si se escoge uno o mas idiomas para el filtro
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
                                    language_minutes["{0}".format(i)] += c.minutes

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
                                language_minutes["{0}".format(i)] += c.minutes
            
        ctx["total_calls"] = calls
        ctx["minutes"] = round(minutes,2)
        ctx["adjust_min"] = round(adjust_min,2)
        ctx["times"] = times
        ctx["language_minutes"] = language_minutes

        return render(request, 'reports/reports_transperfect_production.html', ctx)
    # Si se escoge uno o mas idiomas para el filtro
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
                                language_minutes["{0}".format(i)] += c.minutes
            
        ctx["total_calls"] = calls
        ctx["minutes"] = round(minutes,2)
        ctx["adjust_min"] = round(adjust_min,2)
        ctx["times"] = times
        ctx["language_minutes"] = language_minutes

        return render(request, 'reports/reports_transperfect_production.html', ctx)

    return render(request, 'reports/reports_transperfect_production.html', ctx)

@login_required
def employees_transperfect_performance(request):
    # Obtener la fecha de las llamadas que se van a registrar en el historial
    date_call_history = request.POST.get('date')
    # Variable que guardara la fecha y hora actual
    timestamp = datetime.now()
    # Variable que guardara la fecha actual
    today = date.today()
    # Variable que guarda los ultimos 7 días
    week = today - timedelta(days=7)
    
    # Contesxto que sera enviado a la vista
    ctx = {
        "today":today.strftime("%Y-%m-%d"),
        "week":week.strftime("%Y-%m-%d"),
    }

    # Si se intentas ingresar datos a la base de datos se intenta validar que los datos esten en el formato correcto
    if (request.method == "POST"):
        # Variable que guarda el archivo que contiene los datos de las llamadas
        file = request.FILES['call-history']
        # EL marco de datos transformado usando la libreria 'pandas'
        df=pd.read_excel(file, skiprows=2)
        
        # Verificar si los datos contienen los tipos de datos y el correcto orden en el que deben estar los datos
        try:
            df.columns=["Unnamed: 0","Unnamed: 1","unavailable - end of shift","available", "Talk Time", "unavailable - acw","unavailable - ring-through","unavailable - break","unavailable - scheduled call","unavailable - meeting","unavailable - lunch"]
        except:
            ctx = {
                "today":today.strftime("%Y-%m-%d"),
                "week":week.strftime("%Y-%m-%d"),
            }
            # En caso de no tener el formato correcto, devoler un mensaje de error
            messages.error(request, 'Some of the data seems to not match with the correct format.')
            return render(request, 'reports/performance_transperfect.html',ctx)
            

        # Validar que los datos esten todos en el formato correcto
        for x in range(len(df["Unnamed: 1"])):
            # Comenzar a validar en la primera linea que tenga los datos correctos
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
                    ctx = {
                        "today":today.strftime("%Y-%m-%d"),
                        "week":week.strftime("%Y-%m-%d"),
                    }
                    # En caso de no tener el formato correcto, devoler un mensaje de error
                    messages.error(request, 'Some of the data seems to not match with the correct format.')
                    return render(request, 'reports/performance_transperfect.html', ctx)
                
                # Validar que el empleado exista en la base de datos
                try:
                    employee = Transperfect.objects.get(transperfect_id=df["Unnamed: 1"][x])
                except:
                    ctx = {
                        "today":today.strftime("%Y-%m-%d"),
                        "week":week.strftime("%Y-%m-%d"),
                    }
                    # En caso de no tener el empleado en la base de datos, devoler un mensaje de error
                    messages.error(request, 'Some of the employees are not in the database.')
                    return render(request, 'reports/performance_transperfect.html', ctx)

        # Agregar los datos a la base de datos
        for x in range(len(df["Unnamed: 1"])):
            if isinstance(df["Unnamed: 1"][x], str):
                employee = Transperfect.objects.get(transperfect_id=df["Unnamed: 1"][x])
                
                # Convertir los datos de tipo 'cadena de texto' a 'número' redondeado a 2 decimales despues del punto

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

                # Asignar los datos transformados
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
                # Guardar esta entrada en historial de llamadas
                calls.save()
        # Enviar un mensaje de exito al subir los datos
        messages.success(request, 'The data has been uploaded.')
        return render(request, 'reports/performance_transperfect.html', ctx)
    return render(request, 'reports/performance_transperfect.html', ctx)

@login_required
def employees_transperfect_production(request):
    # Variable que guardara la fecha y hora actual
    timestamp = datetime.now()

    # Si se intentas ingresar datos a la base de datos se intenta validar que los datos esten en el formato correcto
    if (request.method == "POST"):
        # Obtener la cantidad a ajustar en todos los minutos que se van a registrar en el historial
        adjust_min = request.POST.get('adjust')

        # Variable que guarda el archivo que contiene los datos de las llamadas
        file = request.FILES['call-history']
        # EL marco de datos transformado usando la libreria 'pandas'
        df=pd.read_excel(file)

        # Verificar si los datos contienen los tipos de datos y el correcto orden en el que deben estar los datos
        try:
            df.columns=["Employee_ID","Full Name","Language", "StartDate", "EndDate","Real Minutes","SpeedOfAnswer"]
        except:
            # En caso de no tener el formato correcto, devoler un mensaje de error
            messages.error(request, 'Some of the data seems to not match with the correct format.')
            return render(request, 'reports/production_transperfect.html')
        
        # Validar que los datos esten todos en el formato correcto
        for x in range(len(df["Employee_ID"])):
            if not(isinstance(df["Employee_ID"][x],str) and isinstance(df["Full Name"][x],str) and isinstance(df["Language"][x],str) and isinstance(df["StartDate"][x],datetime) and isinstance(df["EndDate"][x],datetime) and isinstance(df["Real Minutes"][x],np.floating) and isinstance(df["SpeedOfAnswer"][x],np.integer)):
                # En caso de no tener el formato correcto, devoler un mensaje de error
                messages.error(request, 'Some of the data seems to not match with the correct format.')
                return render(request, 'reports/production_transperfect.html')
            
            if isinstance(df["Employee_ID"][x], str):
                # Validar que el empleado exista en la base de datos
                try:
                    employee = Transperfect.objects.get(transperfect_id=df["Employee_ID"][x])
                except:
                    # En caso de no tener el empleado en la base de datos, devoler un mensaje de error
                    messages.error(request, 'Some of the employees are not in the database.')
                    return render(request, 'reports/production_transperfect.html')
        
        # Ingresar los datos a la base de datos
        for x in range(len(df["Employee_ID"])):
            if isinstance(df["Employee_ID"][x], str):
                employee = Transperfect.objects.get(transperfect_id=df["Employee_ID"][x])
                
                # Guardar los datos transformados en variables

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
                
                # Asignar los datos transformados
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
                # Guardar esta entrada en historial de llamadas
                calls.save()

        # Enviar un mensaje de exito al subir los datos
        messages.success(request, 'The data has been uploaded.')
        return render(request, 'reports/production_transperfect.html')
    return render(request, 'reports/production_transperfect.html')

@login_required
def employees_propio(request):
    # Variable que guarda todos los empleados
    Employees = Propio.objects.all()
    # Variable que guardara la fecha y hora actual
    timestamp = datetime.now()

    # Si se intentas ingresar datos a la base de datos se intenta validar que los datos esten en el formato correcto
    if (request.method == "POST"):
        # Obtener el ID empleado del que pertenecen los datos
        emp_id = request.POST.get('employee')
        # Obtener el empleado del que pertenecen los datos
        employee = Propio.objects.get(employee_id=emp_id)
        # Variable que guarda el archivo que contiene los datos de las llamadas
        file = request.FILES['call-history']
        # EL marco de datos transformado usando la libreria 'pandas'
        df=pd.read_excel(file)

        # Verificar si los datos contienen los tipos de datos y el correcto orden en el que deben estar los datos
        try:
            df.columns=["LABEL-1","LABEL-2","LABEL-3", "LABEL-4", "LABEL-5","LABEL-6","LABEL-7"]
        except:
            # En caso de no tener el formato correcto, devoler un mensaje de error
            messages.error(request, 'Some of the data seems to not match with the correct format.')
            ctx = {
                "Employees": Employees,
            }
            return render(request, 'reports/employees_propio.html', ctx)
       
        # Validar que los datos esten todos en el formato correcto
        for x in range(len(df["LABEL-1"])):
            if not(isinstance(df["LABEL-2"][x],str) and isinstance(df["LABEL-3"][x],datetime) and isinstance(df["LABEL-4"][x],time) and isinstance(df["LABEL-5"][x],time)):
                # En caso de no tener el formato correcto, devoler un mensaje de error
                messages.error(request, 'Some of the data seems to not match with the correct format.')
                ctx = {
                    "Employees": Employees,
                }
                return render(request, 'reports/employees_propio.html', ctx)

        # Ingresar los datos a la base de datos
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
            
            # Asignar los datos transformados
            calls = Propio_CallHistory(
                employee_id = employee,
                interaction_date  = (df["LABEL-3"][x]),
                interaction_start_time = datetime_formated,
                interaction_length = lenght,
                interaction_length_minutes = ((df["LABEL-5"][x].hour * 60) + df["LABEL-5"][x].minute),
                created = timestamp,
            )
            # Guardar esta entrada en historial de llamadas
            calls.save()

        # Enviar un mensaje de exito al subir los datos
        messages.success(request, 'The data has been uploaded.')
        ctx = {
            "Employees": Employees,
        }
        return render(request, 'reports/employees_propio.html', ctx)

    # Contexto que sera enviado a la vista
    ctx = {
        "Employees": Employees,
    }
    return render(request, 'reports/employees_propio.html', ctx )

@login_required
def get_employee_propio(request):
    # Variable que guarda todos los empleados
    Employees = Propio.objects.all()
    # Variable que guarda todos las ciudades en la base de datos
    Cities = City.objects.all()
    # Variable que guarda el tipo de cuenta al que pertenecera el empleado
    Skillsets = Skillset.objects.get(skillset='MSI PR')

    # Si se intentas ingresar datos a la base de datos se intenta validar que los datos esten en el formato correcto
    if (request.method == "POST"):
        # Obtener el ID empleado del que pertenecen los datos
        employee_id = request.POST.get('employee_id')
        # Obtener el ID Propio del que pertenecen los datos
        propio_id = request.POST.get('propio_id')
        # Obtener el Primer nombre del empleado
        first_name = request.POST.get('first_name')
        # Obtener el Segundo nombre del empleado
        middle_name = request.POST.get('middle_name')
        # Obtener el Apellido del empleado
        last_names = request.POST.get('last_names')
        # Obtener la ciudad a la que pertenece el empleado
        city = request.POST.get('city')
        # Obtener los datos de la ciudad
        city_id = City.objects.get(city=city)

        # Verificar si los datos estan en el formato esperado
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
            # Guardar los datos en la base de datos
            employee.save()
        except:
            # En caso de no tener el formato correcto, devoler un mensaje de error
            messages.error(request, "It seems that either the Employee ID or the Propio ID were already in use.")
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
        # Enviar un mensaje de exito al subir los datos
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
    # Variable que guarda todos los empleados
    Employees = Transperfect.objects.all()
    # Variable que guarda todos las ciudades en la base de datos
    Cities = City.objects.all()
    # Variable que guarda tipo de cuentas al que pertenecera el empleado
    Skillsets = Skillset.objects.get(skillset='MSI TP')

    # Si se intentas ingresar datos a la base de datos se intenta validar que los datos esten en el formato correcto
    if (request.method == "POST"):
        # Obtener el ID empleado del que pertenecen los datos
        employee_id = request.POST.get('employee_id')
        # Obtener el ID Transperfect del que pertenecen los datos
        transperfect_id = request.POST.get('transperfect_id')
        # Obtener el Primer nombre del empleado
        first_name = request.POST.get('first_name')
        # Obtener el Segundo nombre del empleado
        middle_name = request.POST.get('middle_name')
        # Obtener el Apellido del empleado
        last_names = request.POST.get('last_names')
        # Obtener la ciudad a la que pertenece el empleado
        city = request.POST.get('city')
        # Obtener los datos de la ciudad
        city_id = City.objects.get(city=city)

        # Verificar si los datos estan en el formato esperado
        try:
            employee = Transperfect(
                employee_id = employee_id,
                first_name  = first_name, 
                middle_name = middle_name,
                last_names = last_names,
                transperfect_id = transperfect_id,
                skillset=Skillsets,
                city=city_id,
            )
            # Guardar los datos en la base de datos
            employee.save()
        except:
            # En caso de no tener el formato correcto, devoler un mensaje de error
            messages.error(request, "It seems that either the Employee ID or the Transperfect ID were already in use.")
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
        # Enviar un mensaje de exito al subir los dato
        messages.success(request, "The employee was successfully added.")
        return render(request, 'employees/transperfect.html', ctx)

    ctx = {
        "Employees":Employees,
        "Cities":Cities,
        "Skillsets":Skillsets,
    }
    return render(request, 'employees/transperfect.html', ctx)

@login_required
def deactivate_employee_propio(request, uid):
    # Encontrar el empleado que se desactivara
    employee = get_object_or_404(Propio, employee_id=uid)
    # Estado binario del empleado que simboliza un empleado desactivado
    employee.employee_active = "0"
    # Guardar el cambia al empleado
    employee.save()

    # Datos que seran enviados a la vista

    Employees = Propio.objects.all()
    Cities = City.objects.all()
    Skillsets = Skillset.objects.get(skillset='MSI PR')

    # Contexto que sera enviado a la vista
    ctx = {
        "Employees":Employees,
        "Cities":Cities,
        "Skillsets":Skillsets,
    }
    return render(request, 'employees/propio.html', ctx)

@login_required
def activate_employee_propio(request, uid):
    # Encontrar el empleado que se activara
    employee = get_object_or_404(Propio, employee_id=uid)
    # Estado binario del empleado que simboliza un empleado activado
    employee.employee_active = "1"
    # Guardar el cambia al empleado
    employee.save()

    # Datos que seran enviados a la vista

    Employees = Propio.objects.all()
    Cities = City.objects.all()
    Skillsets = Skillset.objects.get(skillset='MSI PR')

    # Contexto que sera enviado a la vista
    ctx = {
        "Employees":Employees,
        "Cities":Cities,
        "Skillsets":Skillsets,
    }
    return render(request, 'employees/propio.html', ctx)

@login_required
def deactivate_employee_transperfect(request, uid):
    # Encontrar el empleado que se desactivara
    employee = get_object_or_404(Transperfect, employee_id=uid)
    # Estado binario del empleado que simboliza un empleado desactivado
    employee.employee_active = "0"
    # Guardar el cambia al empleado
    employee.save()

    # Datos que seran enviados a la vista

    Employees = Transperfect.objects.all()
    Cities = City.objects.all()
    Skillsets = Skillset.objects.get(skillset='MSI TP')

    # Contexto que sera enviado a la vista
    ctx = {
        "Employees":Employees,
        "Cities":Cities,
        "Skillsets":Skillsets,
    }
    return render(request, 'employees/transperfect.html', ctx)

@login_required
def activate_employee_transperfect(request, uid):
    # Encontrar el empleado que se activara
    employee = get_object_or_404(Transperfect, employee_id=uid)
    # Estado binario del empleado que simboliza un empleado activado
    employee.employee_active = "1"
    # Guardar el cambia al empleado
    employee.save()

    # Datos que seran enviados a la vista

    Employees = Transperfect.objects.all()
    Cities = City.objects.all()
    Skillsets = Skillset.objects.get(skillset='MSI TP')

    # Contexto que sera enviado a la vista
    ctx = {
        "Employees":Employees,
        "Cities":Cities,
        "Skillsets":Skillsets,
    }
    return render(request, 'employees/transperfect.html', ctx)

