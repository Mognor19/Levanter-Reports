from datetime import datetime, date, timedelta
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from app_reportes.models import *
from django.contrib.auth.decorators import login_required

@login_required
def record(request):
    # Lista del historia de llamadas de la cuenta Trasnperfect del lado de produccion, organizado por fecha de creación
    Tp_production_history = Production_Transperfect_CallHistory.objects.values_list('pk','employee_id__skillset__skillset','created')
    # Lista del historia de llamadas de la cuenta Trasnperfect del lado de rendimiento, organizado por fecha de creación
    Tp_performance_history = Transperfect_CallHistory.objects.values_list('pk','employee_id__skillset__skillset','created')
    # Lista del historia de llamadas de la cuenta Propio, organizado por fecha de creación
    Pr_history = Propio_CallHistory.objects.values_list('pk','employee_id__skillset__skillset','created')
    # Contador que detendra el programa al llegar a 100
    count = 0

    # Contexto que sera enviado a la plantilla
    ctx = {}

    # Adding the 3 types of call history's to the context
    for x in range(3):
        if x == 0:
            ctx["data"] = Tp_production_history
        elif x == 1:
            ctx["data"] = ctx['data'].union(Tp_performance_history, all=True)
        else:
            ctx["data"] = ctx['data'].union(Pr_history, all=True)
    
    # Rearrange the data to show the most recent first
    ctx['data'] = ctx['data'].order_by('-created')

    # Using the previous data to create a single log
    for x in ctx['data']:
        count += 1
        skillsets = Skillset.objects.get(skillset = x[1])
        timestamp = x[2]

        if Transperfect_CallHistory.objects.filter(pk=x[0],employee_id__skillset = skillsets,created=timestamp):
            if 'history' not in ctx:
                ctx["history"] = [Transperfect_CallHistory.objects.filter(pk=x[0],employee_id__skillset = skillsets,created=timestamp)]
            else:
                ctx['history'].insert(0,Transperfect_CallHistory.objects.filter(pk=x[0],employee_id__skillset = skillsets,created=timestamp))
        
        elif Production_Transperfect_CallHistory.objects.filter(pk=x[0],employee_id__skillset = skillsets,created=timestamp):
            if 'history' not in ctx:
                ctx["history"] = [Production_Transperfect_CallHistory.objects.filter(pk=x[0],employee_id__skillset = skillsets,created=timestamp)]
            else:
                ctx['history'].insert(0,Production_Transperfect_CallHistory.objects.filter(pk=x[0],employee_id__skillset = skillsets,created=timestamp))
        
        elif Propio_CallHistory.objects.filter(pk=x[0],employee_id__skillset = skillsets,created=timestamp):
            if 'history' not in ctx:
                ctx["history"] = [Propio_CallHistory.objects.filter(pk=x[0],employee_id__skillset = skillsets,created=timestamp)]
            else:
                ctx['history'].insert(0,Propio_CallHistory.objects.filter(pk=x[0],employee_id__skillset = skillsets,created=timestamp))
        else:
            ctx['history'] = {}
        
        if count == 100:
            break


    return render(request, 'record/record.html', ctx)

    