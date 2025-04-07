# students/urls.py
from django.urls import path
from .views import student_list
from .views import student_add
from .views import student_edit
from .views import mark_attendance
from .views import view_attendance
from . import views
from .views import StudentListCreateAPIView, AttendanceListCreateAPIView, CourseListCreateAPIView




urlpatterns = [
    path('', student_list, name='student_list'),
    path('add/', student_add, name='student_add'),
    path('edit/<int:pk>/', student_edit, name='student_edit'),
    path('attendance/mark/', mark_attendance, name='mark_attendance'),
    path('attendance/view/', view_attendance, name='view_attendance'),
    path('add-course/', views.add_course, name='add_course'),
    path('course-list/', views.course_list, name='course_list'),
    path('students/', StudentListCreateAPIView.as_view(), name='student-list-create'),
    path('attendance/', AttendanceListCreateAPIView.as_view(), name='attendance-list-create'),
    path('courses/', CourseListCreateAPIView.as_view(), name='course-list-create'),
]
