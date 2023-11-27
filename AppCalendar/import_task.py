import csv
import icalendar
from datetime import datetime, time
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Task

def read_csv(csv_file):
    task_list = []
    dupe_task_list = []
    
    reader = csv.DictReader(csv_file)
    for row in reader:
        title = row.get('Subject')
        start_date = row.get('Start Date')
        start_time = row.get('Start Time')
        end_date = row.get('End Date')
        end_time = row.get('End Time')
        description = row.get('Description')
        
    start_datetime = datetime.strptime(f'{start_date} {start_time}', '%Y-%m-%d %H:%M:%S')
    end_datetime = datetime.strptime(f'{end_date} {end_time}', '%Y-%m-%d %H:%M:%S')
    
    formatted_start_time = start_datetime.strftime('%Y-%m-%dT%H:%M')
    formatted_end_time = end_datetime.strftime('%Y-%m-%dT%H:%M')
    
    existing_task = Task.objects.filter(
        title = title, 
        start_time = formatted_start_time, 
        end_time = formatted_end_time
        ).first()
    
    if existing_task:
        dupe_task_list.append(existing_task)
    else:
        task_list.append(Task(
            title = title,
            start_time = formatted_start_time,
            end_time = formatted_end_time,
            description = description
        ))
        
        return task_list, dupe_task_list
        
            