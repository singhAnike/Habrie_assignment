# forms.py
from django import forms
from .models import Student, Parent, AcademicDetails, Document

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        exclude = ['student']


class AcademicDetailsForm(forms.ModelForm):
    class Meta:
        model = AcademicDetails
        exclude = ['student', 'enrollment_id']


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        exclude = ['student']
