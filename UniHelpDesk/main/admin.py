from django.contrib import admin
from .models import Student, Faculty, Staff, Course, Course_Content, Announcement, Complain, Payment


def show_message(modeladmin, request, queryset):
    queryset.update(status='read')

# Register your models here.
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Staff)
admin.site.register(Course)
admin.site.register(Course_Content)
admin.site.register(Announcement)
admin.site.register(Complain)
admin.site.register(Payment)


