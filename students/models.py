# students/models.py
# from .models import Course 

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# from phonenumber_field.modelfields import PhoneNumberField

class Student(models.Model):
    # course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    
    # phone_no = PhoneNumberField(blank=True, null=True)
    # phone = models.IntegerField()
    
    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    status = models.BooleanField()  # True for present, False for absent
    # course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.name} - {self.date} - {'Present' if self.status else 'Absent'}"

class Course(models.Model):
    # name = models.CharField(max_length=100) 
    course_code = models.CharField(max_length=10, unique=True)
    course_name = models.CharField(max_length=100)
    description = models.TextField()
    students = models.ManyToManyField(Student, related_name='courses')  # Many-to-many relationship
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')
    def __str__(self):
        return self.course_name
    
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=True)  # Admin flag for checking user rights
    
    def __str__(self):
        return f"{self.user.username} - Admin"


# models.py
# models.py
class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE) 
    marks = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return f"{self.student.name} - {self.course.course_name} - {self.marks} - {self.year}"

# changes