from django.contrib import admin

from .models import Schedule, Task

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ['task_id', 'category', 'priority', 'title', 'description', 'start_time', 'end_time','address','get_weather']
    
 #def get_weather(self, obj):
        #return obj.weather if obj.weather else "Weather information not available"

    #get_weather.short_description = 'Weather'

admin.site.register(Task,TaskAdmin)
admin.site.register(Schedule)
