from rest_framework import serializers
from .models import Student, Attendance, Course

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'age', 'email']  # Add any other fields you want

class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()  # Nested student data

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'date', 'status']

class CourseSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)

    class Meta:
        model = Course
        fields = [ 'course_code', 'course_name', 'description', 'students']
