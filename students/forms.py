# students/forms.py
from django import forms
from .models import Student, Course
from .models import Admin,Marks

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'email']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'course_name', 'description']

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['is_admin']

class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = [ 'marks', 'year']

