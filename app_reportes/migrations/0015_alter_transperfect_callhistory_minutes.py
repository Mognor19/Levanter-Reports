# Generated by Django 3.2.3 on 2022-04-17 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_reportes', '0014_transperfect_callhistory_minutes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transperfect_callhistory',
            name='minutes',
            field=models.FloatField(blank=True, null=True),
        ),
    ]