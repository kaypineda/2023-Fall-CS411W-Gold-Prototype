import calendar
from collections import defaultdict
from datetime import date, datetime, timedelta

from django.db.models.functions import TruncDate
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import generic

from .forms import TaskForm
from .models import *
from .models import Task
from .utils import Calendar


class CalendarView(generic.ListView):
    model = Task
    template_name = 'AppCalendar/calendar.html'

    def get_context_data(self, **kwargs):
        """
        Get calendar data

        Parameters:
            self: class instance
            **kwargs: Additonal keyword arguments
        Returns:
            context
        """
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        
        # Fetches a weeks worth of tasks
        today = datetime.today()
        start_week = today - timedelta(days=today.weekday() + 1)
        end_week = start_week + timedelta(days=6)
        tasks = Task.objects.annotate(
            end_date=TruncDate('end_time')
        ).filter(
            end_date__range=[
                start_week,
                end_week
        ]).order_by('priority', 'end_time')
        
        tasks_to_reschedule = []
        tasks_by_date = defaultdict(list)
        for task in tasks:
            tasks_by_date[task.end_date].append(task)
        for tasks_on_same_date in tasks_by_date.values():
            tasks_by_priority = defaultdict(list)
            for task in tasks_on_same_date:
                tasks_by_priority[task.priority].append(task)
            for tasks_with_same_priority in tasks_by_priority.values():
                if len(tasks_with_same_priority) > 1:
                    tasks_to_reschedule.extend(task.task_id for task in tasks_with_same_priority)

                    
        context['task_list'] = tasks
        context['tasks_to_reschedule'] = tasks_to_reschedule
        
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def task(request, task_id=None):
    """
    Adding/editing a task to user schedule. Check for existing tasks, and
    saves task otherwise. 

    Parameters:
        request: The HTTP request object.
        task_id: ID of task 

    Returns:
        AppCalendar/reschedule.html prompt if there is overlapping tasks,
        saves task to schedule otherwise
    """
    instance = Task()
    if task_id:
        instance = get_object_or_404(Task, pk=task_id)
    else:
        instance = Task()

    form = TaskForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        
        #print("Entering prioritize function!!")

        form.save()

        msg = ""
        tasks = Task.objects.exclude(pk=instance.pk)
        if tasks.exists():
            for task in tasks:
                overlap = instance.check_overlap(task.start_time, task.end_time, instance.start_time, instance.end_time)
                #print(overlap)
                if overlap:
                    if instance.priority < task.priority: # lower number is higher priority
                        msg = "This task conflicts with a task of a lower priority."
                    elif instance.priority > task.priority:
                        msg = "This task conflicts with a task of a higher priority."
                    else:
                        msg = "This task conflicts with another task."
                    return render(request, 'AppCalendar/reschedule.html', {'task': instance, 'overlap_task': task, 'message': msg})
        
        return HttpResponseRedirect(reverse('AppCalendar:calendar'))   
    #print("Returning to form.")        
    return render(request, 'AppCalendar/task.html', {'form': form})


def task_delete(request, task_id=None):
    """
    Allows the user to delete a task.

    Parameters:
        request: The HTTP request object.
        task_id: ID of task to be deleted

    Returns: 
        Task deletion prompt
    """
    instance = Task.objects.get(pk=task_id)

    if request.method == 'POST':
        instance.delete()
        return HttpResponseRedirect(reverse('AppCalendar:calendar'))

    return render(request, 'AppCalendar/delete.html', {'task': instance})

