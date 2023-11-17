import csv
import icalendar
from datetime import datetime, time
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Task

def export(request):
    if request.method == 'POST':
        format = request.POST.get('format')

    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="schedule.csv"'

        writer = csv.writer(response)
        writer.writerow(['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 
                         'All Day Event', 'Description', 'Location', 'Private'])
        
        for task in Task.objects.all().values_list('title', 'start_time', 'end_time','description'):
            start_time = task[1].time()
            end_time = task[2].time() 

            all_day_event = 'True' if start_time == time(0,0) and end_time == time(23,59,59) else 'False'
            writer.writerow([task[0], task[1].date(), start_time.strftime('%H:%M:%S'), task[2].date(), end_time.strftime('%H:%M:%S'),
                             all_day_event, task[3], '', ''])
        return response
    
    elif format == 'ics':
        response = HttpResponse(content_type='text/calendar')
        response['Content-Disposition'] = 'attachment; filename="schedule.ics"'
        
        cal = icalendar.Calendar()
        cal.add('prodid', '-//Schedule Puzzle//EN')
        cal.add('version', '2.0')
             
        tasks = Task.objects.all()
        for task in tasks:
            ical_task = icalendar.Event()

            start_time_naive = task.start_time.replace(tzinfo=None)
            end_time_naive = task.end_time.replace(tzinfo=None)
           
            ical_task.add('uid', task.task_id)
            ical_task.add('summary', task.title)
            ical_task.add('dtstart', start_time_naive)
            ical_task.add('dtend', end_time_naive)
            ical_task.add('dtstamp', datetime.now())
            ical_task.add('description', task.description)

            cal.add_component(ical_task)
            print(f"Added event: {task.title}, Start: {task.start_time}, End: {task.end_time}")
    
        response.write(cal.to_ical())

        return response

    return redirect('AppCalendar:calendar')