from django.db import models
from django.conf import settings
from django.urls import reverse

class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    schedule_name = models.CharField(max_length=200)
    schedule_source = models.CharField(max_length=200)

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)

#TODO: ask about variable names
class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    schedule_id = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=200)
    task_source = models.CharField(max_length=200)
    start_date = models.DateField()
    due_date = models.DateField()
    notes = models.TextField() # description?
    category = models.CharField(max_length=200)


#class Event(models.Model):
#    title = models.CharField(max_length=200)
#    description = models.TextField()
#    start_time = models.DateTimeField()
#    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('AppCalendar:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.task_name} </a>'