import csv
import icalendar
from datetime import datetime, time
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Task

def export(request):
    
    """
    Exports tasks in CSV or ICS format based on the user's selection.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Returns a CSV or ICS file as an attachment for download,
                      or redirects to the 'calendar' view if the format is not specified.

    Raises:
        None

    Example:
        To use this function, send a POST request with the 'format' parameter
        specifying either 'csv' or 'ics' to export tasks in the desired format.
    """
    
    if request.method == 'POST':
        # Get the export format from the POST parameters
        format = request.POST.get('format')

    if format == 'csv':
        # Export tasks in CSV format
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="schedule.csv"'

        # Create CSV writer and write header row
        writer = csv.writer(response)
        writer.writerow(['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 
                         'All Day Event', 'Description', 'Location', 'Private'])
        
        # Iterate over tasks and write each row to the CSV file
        for task in Task.objects.all().values_list('title', 'start_time', 'end_time','description'):
            start_time = task[1].time()
            end_time = task[2].time() 

            # Determine if the task is an all-day event
            all_day_event = 'True' if start_time == time(0,0) and end_time == time(23,59,59) else 'False'
            
            # Write task details to the CSV file
            writer.writerow([task[0], task[1].date(), start_time.strftime('%H:%M:%S'), task[2].date(), end_time.strftime('%H:%M:%S'),
                             all_day_event, task[3], '', ''])
        return response
    
    elif format == 'ics':
        # Export tasks in ICS format
        response = HttpResponse(content_type='text/calendar')
        response['Content-Disposition'] = 'attachment; filename="schedule.ics"'
        
        # Create an ICS calendar
        cal = icalendar.Calendar()
        cal.add('prodid', '-//Schedule Puzzle//EN')
        cal.add('version', '2.0')
        
        # Iterate over tasks and add each as an ICS event
        tasks = Task.objects.all()
        for task in tasks:
            ical_task = icalendar.Event()

            # Generate a unique identifier for the ICS event
            uid = f"{task.title}_{task.task_id}_{task.start_time.replace(tzinfo=None)}"
            
            # Convert datetime objects to naive datetime objects for ICS
            start_time_naive = task.start_time.replace(tzinfo=None)
            end_time_naive = task.end_time.replace(tzinfo=None)
            
            # Set ICS event properties
            # ical_task.add('uid', task.task_id)
            ical_task.add('uid', uid)
            ical_task.add('summary', task.title)
            ical_task.add('dtstart', start_time_naive)
            ical_task.add('dtend', end_time_naive)
            ical_task.add('dtstamp', datetime.now())
            ical_task.add('description', task.description)

            # Add the ICS event to the calendar
            cal.add_component(ical_task)
            print(f"Added event: {task.title}, Start: {task.start_time}, End: {task.end_time}")

        # Write the ICS calendar to the response
        response.write(cal.to_ical())

        return response

    # Redirect to the 'calendar' view if the format is not specified
    return redirect('AppCalendar:calendar')