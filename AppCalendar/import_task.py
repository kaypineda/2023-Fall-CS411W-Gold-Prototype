import csv
import icalendar
from datetime import datetime, time
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Task

def read_csv(csv_file):
    tasks_list = []
    duplicate_list = []
    
    reader = csv.DictReader(csv_file)
    for row in reader:
        title = row.get('Subject')
        start_date = row.get('Start Date')
        start_time = row.get('Start Time')
        end_date = row.get('End Date')
        end_time = row.get('End Time')
        description = row.get('Description')
        
            