# Generated by Django 4.2.6 on 2023-10-25 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppCalendar', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='schedule_attributes',
        ),
    ]
