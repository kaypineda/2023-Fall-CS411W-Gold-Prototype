from django.contrib import admin

from .models import Schedule, Task

# Register your models here.
admin.site.register(Task)
admin.site.register(Schedule)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['task_id', 'category', 'priority', 'title', 'description', 'start_time', 'end_time']
