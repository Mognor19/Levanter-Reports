# Generated by Django 3.2.3 on 2022-03-03 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(blank=True, max_length=6, null=True, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_names', models.CharField(blank=True, max_length=50, null=True)),
                ('interpreter_id', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
