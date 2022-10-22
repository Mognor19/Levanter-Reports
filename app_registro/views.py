from datetime import datetime, date, timedelta
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from app_reportes.models import *
from django.contrib.auth.decorators import login_required

@login_required
def record(request):
    Tp_production_history = Production_Transperfect_CallHistory.objects.values_list('pk','employee_id__skillset__skillset','created')
    Tp_performance_history = Transperfect_CallHistory.objects.values_list('pk','employee_id__skillset__skillset','created')
    Pr_history = Propio_CallHistory.objects.values_list('pk','employee_id__skillset__skillset','created')
    count = 0
    ctx = {}

    for x in range(3):
        if x == 0:
            ctx["data"] = Tp_production_history
        elif x == 1:
            ctx["data"] = ctx['data'].union(Tp_performance_history, all=True)
        else:
            ctx["data"] = ctx['data'].union(Pr_history, all=True)
    
    ctx['data'] = ctx['data'].order_by('-created')

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

    