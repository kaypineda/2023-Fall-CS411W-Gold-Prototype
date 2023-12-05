import csv
from datetime import datetime

import icalendar
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone

from .models import Task


def import_file(request):
    
    """
    Imports tasks from CSV or ICS files and saves them to the Task model.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the 'calendar' view upon successful import,
                      or returns an error message if the file type is not supported.

    Raises:
        None

    Example:
        To use this function, send a POST request with a CSV or ICS file attached
        using the 'csv_file' or 'ics_file' form fields.
    """
    
    if request.method == 'POST':
        # Get uploaded files from the request
        csv_file = request.FILES.get('csv_file')
        ics_file = request.FILES.get('ics_file')
        
        # Create a list to store all duplicate tasks
        duplicate_task_list = []
        
        # Import from CSV file
        if csv_file is not None:
            if not csv_file.name.endswith('.csv'):
                return HttpResponse('No CSV file found.')

            # Read CSV file and create tasks
            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
        
            for row in reader:
                title = row.get('Subject')
                start_date = row.get('Start Date')
                start_time = row.get('Start Time')
                end_date = row.get('End Date')
                end_time = row.get('End Time')
                description = row.get('Description')
                 
                # Convert date and time strings to datetime objects
                start_datetime = datetime.strptime(f'{start_date} {start_time}', '%Y-%m-%d %H:%M:%S')
                end_datetime = datetime.strptime(f'{end_date} {end_time}', '%Y-%m-%d %H:%M:%S')

                # Format datetime objects as strings for the Task model
                start_datetime = timezone.make_aware(start_datetime)
                end_datetime = timezone.make_aware(end_datetime)
                

                # Check for duplicate tasks
                duplicate_tasks = Task.objects.filter(
                    title=title,
                    start_time=start_datetime,
                    end_time=end_datetime
                )
                if duplicate_tasks.exists():
                    duplicate_task_list.append(title)
                    continue
                    # duplicate_task_list.extend(list(duplicate_tasks))
                
                else:            
                    # Create and save a new Task object
                    new_task = Task(
                        title = title,
                        start_time = start_datetime,
                        end_time = end_datetime,
                        description = description
                    )
                    
                    new_task.save()
            
        # Import from ICS file
        if ics_file is not None:
            if not ics_file.name.endswith('.ics'):
                return HttpResponse('No ICS file found.')

            # Parse ICS file and create tasks
            cal = icalendar.Calendar.from_ical(ics_file.read())
            
            
            for component in cal.walk():
                if component.name == 'VEVENT':
                    title = component.get('summary').to_ical().decode('utf-8')
                    start_time = component.get('dtstart').dt
                    end_time = component.get('dtend').dt
                    description = component.get('description')
                    
                    # Check for duplicate tasks
                    duplicate_tasks = Task.objects.filter(
                        title = title,
                        start_time = start_time,
                        end_time = end_time
                    )
                    if duplicate_tasks.exists():
                        # duplicate_task_list.extend(list(duplicate_tasks))
                        duplicate_task_list.append(title)
                        continue
                    
                    else:                   
                        new_task = Task(
                            title = title,
                            start_time = start_time,
                            end_time = end_time,
                            description = description
                        )
                        new_task.save()
        if duplicate_task_list:
            # Display warning message and provide options to schedule or delete duplicate tasks
            # return render(request, 'AppCalendar/duplicate_import.html', {'duplicate_tasks': duplicate_task_list})   
            messages.warning(request, f'There are duplicate tasks in your file that have been skipped: {duplicate_task_list}')      
        # Redirect to the 'calendar' view after successful import           
        return redirect('AppCalendar:calendar')
    
    else:
        # Return an error message if the request method is not POST
        return HttpResponse('File not uploaded.')

        
            