from django.contrib import admin

# Register your models here.
# devops/admin.py

from django.contrib import admin
from .models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'trainer', 'course_name', 'created_at')
    search_fields = ('student__username', 'trainer__username', 'course_name')
    list_filter = ('course_name', 'created_at')
