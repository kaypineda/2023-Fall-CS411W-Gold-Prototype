from django.db import models
from AppUser.models import AppUser

# Create your models here.
class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    schedule_name = models.CharField(max_length=200)
    schedule_source = models.CharField(max_length=200)
    schedule_attributes = models.TextField()
