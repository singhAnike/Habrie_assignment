from django.shortcuts import render, redirect
from .forms import StudentForm, ParentForm, AcademicDetailsForm, DocumentForm, CSVUploadForm
from django.db import transaction
from random import randint
from .models import Student, Parent, Document, AcademicDetails
from django.contrib import messages
import csv
from datetime import datetime
from django.db.utils import IntegrityError
from django.views.generic import ListView
from django.db.models import Count
from tablib import Dataset
from .resources import StudentResource 
from django.http import HttpResponse
from django.views.generic import View
from django.core.mail import send_mail



# task-5
def enroll_student(student):

    student_mail_subject = 'Welcome to Dummy School'
    student_mail_message = f"Dear {student.name},\n\nYou have been enrolled in Dummy School. Your Enrollment ID is {student.academic_details.enrollment_id}. Please provide us with the required documents for future references.\n\nTeam Dummy School"
    send_mail(student_mail_subject, student_mail_message, 'from@example.com', [student.mail_id])

    admin_mail_subject = 'New Student Enrollment'
    admin_mail_message = f"Dear Admin,\n\nA new student, {student.name}, has been enrolled in class {student.academic_details.class_name}, section {student.academic_details.section} with enrollment ID {student.academic_details.enrollment_id} in the current session.\n\nBot Msg"
    send_mail(admin_mail_subject, admin_mail_message, 'from@example.com', ['durganand.jha@habrie.com'])

    return {'success': True, 'message': 'Enrollment process completed successfully.'}

def add_student(request):
    success_message = None

    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        parent_form = ParentForm(request.POST)
        academic_details_form = AcademicDetailsForm(request.POST)
        document_form = DocumentForm(request.POST, request.FILES)

        if all([student_form.is_valid(), parent_form.is_valid(), academic_details_form.is_valid(), document_form.is_valid()]):
            with transaction.atomic():
                student = student_form.save()
                parent = parent_form.save(commit=False)
                parent.student = student
                parent.save()

                academic_details = academic_details_form.save(commit=False)
                academic_details.student = student
                academic_details.enrollment_id = generate_enrollment_id(student)
                academic_details.save()

                document = document_form.save(commit=False)
                document.student = student
                document.save()

                # Call the enrollment logic here
                enrollment_result = enroll_student(student)
                if enrollment_result['success']:
                    success_message = enrollment_result['message']
                    messages.success(request, success_message)
                else:
                    messages.error(request, "Enrollment process failed. Please contact the admin.")

            success_message = "Data posted successfully!"

    
            messages.success(request, success_message)
        else:
            messages.error(request, "Form validation failed. Please check your input.")

    else:
        student_form = StudentForm()
        parent_form = ParentForm()
        academic_details_form = AcademicDetailsForm()
        document_form = DocumentForm()

    return render(request, 'add_student.html', {
        'student_form': student_form,
        'parent_form': parent_form,
        'academic_details_form': academic_details_form,
        'document_form': document_form,
        'success_message': success_message,
    })

def generate_enrollment_id(student):
    return f"{student.dob.strftime('%d%m%y')}{student.name[:3].upper()}{randint(1, 999):03}"

def handle_uploaded_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']

        try:
            with transaction.atomic():
                
                csv_data = csv.DictReader(csv_file.read().decode('utf-8').splitlines())

                enrollment_id = ""
                for row in csv_data:                    
                    dob = datetime.strptime(row.get('dob', '2000-01-01'), '%Y-%m-%d').date()
                    date_of_joining = datetime.strptime(row.get('date_of_joining', '2000-01-01'), '%Y-%m-%d').date()

                    student_data = {k: row[k] for k in Student._meta.fields if k in row}
                    student_data['dob'] = dob
                    student = Student.objects.create(**student_data)

                    parent_data = {k: row[k] for k in Parent._meta.fields if k in row}
                    parent_data['student'] = student
                    parent = Parent.objects.create(**parent_data)

                    academic_data = {k: row[k] for k in AcademicDetails._meta.fields if k in row}
                    academic_data['student'] = student
                    academic_data['date_of_joining'] = date_of_joining

                    enrollment_id = academic_data.get('enrollment_id')
                    enrollment_id = "" 
                    while AcademicDetails.objects.filter(enrollment_id=enrollment_id).exists():
                            enrollment_id += "_duplicate"

                    while AcademicDetails.objects.filter(enrollment_id=enrollment_id).exists():
                        enrollment_id += "_duplicate"

                    academic_data['enrollment_id'] = enrollment_id

                    academic = AcademicDetails.objects.create(**academic_data)

                    document_data = {k: row[k] for k in Document._meta.fields if k in row}
                    document_data['student'] = student
                    document = Document.objects.create(**document_data)

                return render(request, 'bulk_upload_csv.html', {'message': 'Data uploaded successfully'})
        except IntegrityError as e:
            return render(request, 'bulk_upload_csv.html', {'error_message': f"Error uploading data: {e}"})

    return render(request, 'bulk_upload_csv.html', {'error_message': 'Invalid request'})

class StudentListView(ListView):
    model = Student
    template_name = 'student_list.html'
    context_object_name = 'students'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch unique values for class, section, and admission category
        context['class_options'] = AcademicDetails.objects.values('class_name').annotate(count=Count('class_name')).order_by('class_name')
        context['section_options'] = AcademicDetails.objects.values('section').annotate(count=Count('section')).order_by('section')
        context['admission_category_options'] = Student.objects.values('admission_category').annotate(count=Count('admission_category')).order_by('admission_category')

        return context

    def get_queryset(self):
        queryset = Student.objects.all()

        class_filter = self.request.GET.get('class_filter')
        section_filter = self.request.GET.get('section_filter')
        admission_category_filter = self.request.GET.get('admission_category_filter')

        if class_filter:
            queryset = queryset.filter(academic_details__class_name=class_filter)
        if section_filter:
            queryset = queryset.filter(academic_details__section=section_filter)
        if admission_category_filter:
            queryset = queryset.filter(admission_category=admission_category_filter)

        return queryset

class ExportDataView(View):
    def get(self, request, *args, **kwargs):
        class_filter = self.request.GET.get('class_filter')
        section_filter = self.request.GET.get('section_filter')
        admission_category_filter = self.request.GET.get('admission_category_filter')

        queryset = Student.objects.all()

        if class_filter:
            queryset = queryset.filter(academic_details__class_name=class_filter)
        if section_filter:
            queryset = queryset.filter(academic_details__section=section_filter)
        if admission_category_filter:
            queryset = queryset.filter(admission_category=admission_category_filter)

        resource = StudentResource()
        dataset = resource.export(queryset)
        
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=exported_data.xls'
        return response
 