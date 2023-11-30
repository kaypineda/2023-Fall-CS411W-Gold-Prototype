import csv
import icalendar
from datetime import datetime, time
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Task

def import_file(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        ics_file = request.FILES.get('ics_file')
        
        if csv_file is not None:
            return HttpResponse('No CSV file found.')
        
            if not csv_file.name.endswith('.csv'):
                return HttpResponse('The uploaded file is not a CSV file.')

        
            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
        
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
                
                new_task = Task(
                    title = title,
                    start_time = formatted_start_time,
                    end_time = formatted_end_time,
                    description = description
                )
                new_task.save()
            
        if ics_file is not None:
            return HttpResponse('No ICS file found.')
        
        cal = icalendar.Calendar.from_ical(ics_file.read().decode('utf-8'))
        
        for component in cal.walk():
            if component.name == 'VEVENT':
                title = component.get('summary')
                start_time = component.get('dtstart').dt
                end_time = component.get('dtend').dt
                description = component.get('description')
                
                new_task = Task(
                    title = title,
                    start_time = start_time,
                    end_time = end_time,
                    description = description
                )
                new_task.save()
            
            
        return redirect('AppCalendar:calendar')
    
    else:
        return HttpResponse('File not uploaded.')
   

# def import_ics(request):
#     if request.method == 'POST':
#         ics_file = request.FILES.get('ics_file')
        
#         if ics_file is None:
#             return HttpResponse('No file was uploaded.')
        
#         if not ics_file.name.endswith('.ics'):
#             return HttpResponse('The uploaded file is not an ICS file.')
        
#         cal = icalendar.Calendar.from_ical(ics_file.read().decode('utf-8'))
        
#         for component in cal.walk():
#             if component.name == 'VEVENT':
#                 title = component.get('summary')
#                 start_time = component.get('dtstart').dt
#                 end_time = component.get('dtend').dt
#                 description = component.get('description')
                
#                 new_task = Task(
#                     title = title,
#                     start_time = start_time,
#                     end_time = end_time,
#                     description = description
#                 )
#                 new_task.save()
            
#         return redirect('AppCalendar:calendar')
#     else:
#         return HttpResponse('File not uploaded.')
            
   
    # task_list = []
    # dupe_task_list = []
    
    #     existing_task = Task.objects.filter(
    #         title = title, 
    #         start_time = formatted_start_time, 
    #         end_time = formatted_end_time
    #         ).first()
        
    #     if existing_task:
    #         dupe_task_list.append(existing_task)
    #     else:
    #         task_list.append(Task(
    #             title = title,
    #             start_time = formatted_start_time,
    #             end_time = formatted_end_time,
    #             description = description
    #         ))
            
    # return task_list, dupe_task_list
        
            