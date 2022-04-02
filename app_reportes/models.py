from enum import unique
from django.db import models

class City(models.Model):
    city = models.CharField(max_length=3,null=True,unique=True, blank=True)

    def __str__(self):
        return f'City: {self.city}'

class Skillset(models.Model):
    skillset = models.CharField(max_length=6,null=True,unique=True, blank=True)

    def __str__(self):
        return f'City: {self.skillset}'
    

# Create your models here.
class Propio(models.Model):
    employee_id = models.CharField(max_length=6,unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_names  = models.CharField(max_length=50, null=True, blank=True)
    propio_id = models.CharField(max_length=50, null=True, blank=True)
    skillset = models.ForeignKey(Skillset, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    employee_active = models.CharField(max_length=1, default="1", null=True, blank=True)
    def __str__(self):
        return f'EID: {self.employee_id} | Employee: {self.first_name} {self.last_names}'

class Propio_CallHistory(models.Model):
    employee_id = models.ForeignKey(Propio, on_delete=models.CASCADE, null=True, blank=True)
    interaction_date = models.DateField(null=True, blank=True)
    interaction_start_time = models.TimeField(null=True, blank=True)
    interaction_length = models.CharField(max_length=9,null=True, blank=True)
    interaction_length_minutes = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return f'{self.interaction_date} '

