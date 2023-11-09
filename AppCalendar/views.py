from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from ics import Calendar, Event
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
import csv 

from .models import *
from .utils import Calendar
from .forms import TaskForm

def index(request):
    return HttpResponse('hello')

class CalendarView(generic.ListView):
    model = Task
    template_name = 'AppCalendar/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
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
    instance = Task()
    if task_id:
        instance = get_object_or_404(Task, pk=task_id)
    else:
        instance = Task()

    form = TaskForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('AppCalendar:calendar'))
    return render(request, 'AppCalendar/task.html', {'form': form})

def export(request, format):
    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="schedule.csv"'

        writer = csv.writer(response)
        writer.writerow(['title', 'description', 'start_time', 'end_time'])
        for task in Task.objects.all().values_list('title', 'description', 'start_time', 'end_time'):
            writer.writerow(task)
        return response
    
    # elif format == 'ics':
    #     response = HttpResponse(content_type='text/calendar')
    #     response['Content-Disposition'] = 'attachment; filename="schedule.ics"'

    #     calendar = Calendar()
    #     for task in Task.objects.all():
    #         event = Event()
    #         event.name = task.title
    #         event.begin=task.start_time.strftime("%Y%m%dT%H%M%S")
    #         calendar.add_component(event)
    #     response = HttpResponse(content_type='text/ics')
    #     response['Content-Disposition'] = 'attachment; filename="schedule.ics"'
    #     return response

    else:
        response.status_code = 404
        response.reason_phrase = 'Invalid file format'

    return response

