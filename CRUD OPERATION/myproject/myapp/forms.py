from django import forms
from .models import Course, Instructor

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = '__all__'