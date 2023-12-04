import calendar
from collections import Counter
from datetime import date, datetime, timedelta
from .models import Task

from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import generic

from .forms import TaskForm
from .models import *
from .utils import Calendar


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
        
        # Hope this fetches a weeks worth of tasks??
        today = datetime.today()
        start_week = today - timedelta(days=today.weekday() + 1)
        end_week = start_week + timedelta(days=6)
        context['task_list'] = Task.objects.annotate(
            end_date=TruncDate('end_time')
        ).filter(
            end_date__range=[
                start_week,
                end_week
        ]).order_by('priority', 'end_time')
        
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
        
        #print("Entering prioritize function!!")
        start_time = form.cleaned_data['start_time']
        title = form.cleaned_data['title']
        category = form.cleaned_data['category']
        duplicateTimes = Task.objects.exclude(pk=instance.pk).filter(
            start_time__date = start_time.date(),
            start_time__time = start_time.time()
        ) 

        if duplicateTimes:
            #print("There are tasks with the same date and times")
            return render(request, 'AppCalendar/popup.html')
        
        form.save()

        tasks = Task.objects.exclude(pk=instance.pk)
        if tasks.exists():
            for task in tasks:
                overlap = instance.check_overlap(task.start_time, task.end_time, instance.start_time, instance.end_time)
                #print(overlap)
                if overlap:
                    return render(request, 'AppCalendar/reschedule.html', {'task': instance, 'overlap_task': task})
        
        return HttpResponseRedirect(reverse('AppCalendar:calendar'))   
    #print("Returning to form.")        
    return render(request, 'AppCalendar/task.html', {'form': form})


def task_delete(request, task_id=None):
    instance = Task.objects.get(pk=task_id)

    if request.method == 'POST':
        instance.delete()
        return HttpResponseRedirect(reverse('AppCalendar:calendar'))

    return render(request, 'AppCalendar/delete.html', {'task': instance})

