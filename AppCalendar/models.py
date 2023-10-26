from django.db import models
from django.conf import settings

# Create your models here.
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
    
class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    task_id = models.ForeignKey('Task', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    notification_time=models.DateTimeField()
    TYPE_CHOICES = [
        ('Email', 'Email'),
        ('Push', 'Push'),
        ('Text', 'Text'),
    ]
    type = models.CharField(max_length=5, choices=TYPE_CHOICES, default='Email')
    time_created = models.DateTimeField(auto_now_add=True)
    time_sent = models.DateTimeField(null=True, blank = True)

class NotificationMessage(models.Model):
    message_id = models.AutoField(primary_key=True)
    notification_id = models.ForeignKey('Notifications', on_delete=models.CASCADE)
    message = models.TextField()