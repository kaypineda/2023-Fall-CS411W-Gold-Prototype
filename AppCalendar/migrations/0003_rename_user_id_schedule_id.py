# Generated by Django 4.2.7 on 2023-11-28 02:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppCalendar', '0002_delete_location_alter_task_end_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='user_id',
            new_name='id',
        ),
    ]
