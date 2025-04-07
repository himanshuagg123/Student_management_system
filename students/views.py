# Create your views here.
# students/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Attendance,Course,Marks
from .forms import CourseForm 
from django.contrib.auth.decorators import login_required

from .forms import StudentForm
from datetime import date
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentSerializer, AttendanceSerializer, CourseSerializer
from rest_framework import generics
from .models import Admin
from .forms import MarksForm



def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})


def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form})

def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form})

def mark_attendance(request):
    students = Student.objects.all()
    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'present_{student.id}') == 'on'
            Attendance.objects.create(student=student, date=date.today(), status=status)
        return HttpResponse('Attendance marked successfully')
    
    return render(request, 'attendance/mark_attendance.html', {'students': students})

# View to view attendance
def view_attendance(request):
    attendances = Attendance.objects.all()
    return render(request, 'attendance/view_attendance.html', {'attendances': attendances})

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')  # Redirect to course list after successful addition
    else:
        form = CourseForm()
    
    return render(request, 'add_course.html', {'form': form})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})


def enroll_student_in_course(request, student_id, course_id):
    student = Student.objects.get(id=student_id)
    course = Course.objects.get(id=course_id)
    
    # Enroll the student in the course
    course.students.add(student)
    return redirect('student_detail', student_id=student.id)


class StudentListCreateAPIView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List and create attendance
class AttendanceListCreateAPIView(APIView):
    def get(self, request):
        attendance = Attendance.objects.all()
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List and create courses
class CourseListCreateAPIView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def add_student(request):
    if request.user.is_authenticated and request.user.admin.is_admin:
        if request.method == 'POST':
            form = StudentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('student_list')  # Redirect to the student list page
        else:
            form = StudentForm()
        return render(request, 'add_student.html', {'form': form})
    else:
        return redirect('home') 


@login_required
def add_marks(request, student_id, course_id):
    student = get_object_or_404(Student, id=student_id)
    course = get_object_or_404(Course, id=course_id)

    # Check if the logged-in user is the teacher for this course
    if request.user != course.teacher:
        return HttpResponse("You are not authorized to assign marks for this course.", status=403)

    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.student = student
            marks.course = course
            marks.teacher = request.user  # Assign logged-in teacher
            marks.save()
            return redirect('student_detail', student_id=student.id)
    else:
        form = MarksForm()

    return render(request, 'add_marks.html', {'form': form, 'student': student, 'course': course})