from django.contrib import admin

from .models import Schedule, Task

# Register your models here.
admin.site.register(Task)
admin.site.register(Schedule)
