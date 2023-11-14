from django.contrib import admin

class TaskAdmin(admin.ModelAdmin):
    list_display = ['task_id', 'category', 'priority', 'title', 'description', 'start_time', 'end_time']
