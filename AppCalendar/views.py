from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserCreationForm, AuthenticationForm

from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe

import calendar

from .models import *
from .utils import Calendar
from .forms import TaskForm

def index(request):
    #return HttpResponse('hello')
    #return render(request, 'AppCalendar/index.html')
    return render(request, 'AppCalendar/index.html')

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

def task_delete(request, task_id=None):
    instance = Task.objects.get(pk=task_id)
    instance.delete()

    if request.method == 'POST':
        instance.delete()
        return HttpResponseRedirect(reverse('AppCalendar:calendar'))
    
    return render(request, 'AppCalendar/delete.html', {'task': instance})

#signup page
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
        else:
            form = UserCreationForm()
        return render(request, 'AppCalendar/registerform.html', {'form': form})
        
#login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                form = LoginForm()
            return render(request, 'AppCalendar/login.html', {'form': form})

#logout page
def user_logout(request):
    logout(request)
    return redirect('login')
