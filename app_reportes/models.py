from enum import unique
from django.db import models

class City(models.Model):
    # Nombre de la ciudad usando solo 3 letras
    city = models.CharField(max_length=3,null=True,unique=True, blank=True)

    def __str__(self):
        return f'City: {self.city}'

class Skillset(models.Model):
    # Nombre de la cuenta con un maximo de 2 letras. Ej: "MSI {2 iniciales representando la cuenta}"
    skillset = models.CharField(max_length=6,null=True,unique=True, blank=True)

    def __str__(self):
        return f'{self.skillset}'

# Empleados de propio
class Propio(models.Model):
    employee_id = models.CharField(max_length=6,unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_names  = models.CharField(max_length=50, null=True, blank=True)
    propio_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    skillset = models.ForeignKey(Skillset, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    employee_active = models.CharField(max_length=1, default="1", null=True, blank=True)
    def __str__(self):
        return f'EID: {self.employee_id} | Employee: {self.first_name} {self.last_names}'

# Empleados de transperfect
class Transperfect(models.Model):
    employee_id = models.CharField(max_length=6,unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_names  = models.CharField(max_length=50, null=True, blank=True)
    transperfect_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    skillset = models.ForeignKey(Skillset, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    employee_active = models.CharField(max_length=1, default="1", null=True, blank=True)
    def __str__(self):
        return f'EID: {self.transperfect_id} | Employee: {self.first_name} {self.last_names}'

# Historia de llamadas de Propio
class Propio_CallHistory(models.Model):
    employee_id = models.ForeignKey(Propio, on_delete=models.CASCADE, null=True, blank=True)
    interaction_date = models.DateField(null=True, blank=True)
    interaction_start_time = models.DateTimeField(null=True, blank=True)
    interaction_length = models.CharField(max_length=9,null=True, blank=True)
    interaction_length_minutes = models.IntegerField(null=True,blank=True)
    created = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f'{self.interaction_date} '

# Historia de llamadas de Transperfect desempeño
class Transperfect_CallHistory(models.Model):
    employee_id = models.ForeignKey(Transperfect, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    shift_eof = models.CharField(max_length=9,null=True, blank=True)
    eof_minutes = models.FloatField(null=True, blank=True)
    shift_available = models.CharField(max_length=9,null=True, blank=True)
    available_minutes = models.FloatField(null=True, blank=True)
    shift_talk_time = models.CharField(max_length=9,null=True, blank=True)
    talk_minutes = models.FloatField(null=True, blank=True)
    shift_acw = models.CharField(max_length=9,null=True, blank=True)
    acw_minutes = models.FloatField(null=True, blank=True)
    shift_ring_through = models.CharField(max_length=9,null=True, blank=True)
    ring_through_minutes = models.FloatField(null=True, blank=True)
    shift_break = models.CharField(max_length=9,null=True, blank=True)
    break_minutes = models.FloatField(null=True, blank=True)
    shift_schedule_call = models.CharField(max_length=9,null=True, blank=True)
    schedule_call_minutes = models.FloatField(null=True, blank=True)
    shift_meeting = models.CharField(max_length=9,null=True, blank=True)
    meeting_minutes = models.FloatField(null=True, blank=True)
    shift_lunch = models.CharField(max_length=9,null=True, blank=True)
    lunch_minutes = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f'Date:{self.date} | EID:{self.employee_id}'

# Historia de llamadas de Transperfect producción
class Production_Transperfect_CallHistory(models.Model):
    employee_id = models.ForeignKey(Transperfect, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    interaction_start_time = models.DateTimeField(null=True, blank=True)
    interaction_end_time = models.DateTimeField(null=True, blank=True)
    language = models.CharField(max_length=20, null=True, blank=True)
    minutes = models.FloatField(null=True, blank=True)
    speed_answer = models.IntegerField(null=True, blank=True)
    adjusted_minutes = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f'Date:{self.date} | EID:{self.employee_id}'

