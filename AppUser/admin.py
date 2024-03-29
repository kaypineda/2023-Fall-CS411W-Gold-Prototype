from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import EmailUser 

class EmailUserAdmin(UserAdmin):
"""
Admin configuration for the EmailUser model.
"""
    model = EmailUser
    ordering = ('email',)

    list_display = ['email', 'is_staff', 'is_active']
    list_filter = ['email', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}),
    )

    readonly_fields = ['last_login', 'date_joined']#to make readonly in the admin interface

admin.site.register(EmailUser, EmailUserAdmin)
