
from django.contrib import admin
from .models import Student,Attendance,Course,Marks



admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(Course)
# admin.site.register(Marks)

class MarksAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'marks', 'year')
    list_filter = ('year', 'course')  # Add filters to make it easier to find marks by course or year

admin.site.register(Marks, MarksAdmin)

