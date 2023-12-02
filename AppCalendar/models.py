from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

# Define a Django model for scheduling
class Schedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    schedule_name = models.CharField(max_length=200)
    schedule_source = models.CharField(max_length=200)

# Define a Django model for tasks
class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=200, default='')
    priority = models.IntegerField(default=1)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)

    # String representation of the Task object, used for display purposes
    def __str__(self):
        return f'{self.category}:   {self.title}'

    # Property method to generate HTML-formatted URLs for task editing and deletion
    @property
    def get_html_url(self):
        url = reverse('AppCalendar:task_edit', args=(self.task_id,))
        delete = reverse('AppCalendar:task_delete', args=(self.task_id,))
        return f'<a href="{url}"> {self.title} </a> | <a href="{delete}">Delete</a>'
    
    # Custom validation method to ensure that the end time is after the start time
    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('Ending time must after starting times')

# Define a Django model for notifications
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

# Define a Django model for notification messages
class NotificationMessage(models.Model):
    message_id = models.AutoField(primary_key=True)
    notification_id = models.ForeignKey('Notifications', on_delete=models.CASCADE)
    message = models.TextField()
