from django.shortcuts import render, redirect
from .forms import StudentForm, ParentForm, AcademicDetailsForm, DocumentForm, CSVUploadForm
from django.db import transaction
from random import randint
from .models import Student, Parent, Document, AcademicDetails
from django.contrib import messages
import csv
from datetime import datetime
from django.db.utils import IntegrityError


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
                
            # Read CSV file and insert data into the database
                csv_data = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
                
                enrollment_id = ""
                for row in csv_data:
                    # Generate random dummy data
                    
                    dob = datetime.strptime(row.get('dob', '2000-01-01'), '%Y-%m-%d').date()
                    date_of_joining = datetime.strptime(row.get('date_of_joining', '2000-01-01'), '%Y-%m-%d').date()

                    # Create Student instance
                    student_data = {k: row[k] for k in Student._meta.fields if k in row}
                    student_data['dob'] = dob
                    student = Student.objects.create(**student_data)

                    # Create Parent instance
                    parent_data = {k: row[k] for k in Parent._meta.fields if k in row}
                    parent_data['student'] = student
                    parent = Parent.objects.create(**parent_data)

                    # Create AcademicDetails instance
                    academic_data = {k: row[k] for k in AcademicDetails._meta.fields if k in row}
                    academic_data['student'] = student
                    academic_data['date_of_joining'] = date_of_joining

                    # Ensure enrollment_id is unique
                    enrollment_id = academic_data.get('enrollment_id')
                    while AcademicDetails.objects.filter(enrollment_id=enrollment_id).exists():
                        enrollment_id += "_duplicate"

                    academic_data['enrollment_id'] = enrollment_id

                    academic = AcademicDetails.objects.create(**academic_data)

                    # Create Document instance
                    document_data = {k: row[k] for k in Document._meta.fields if k in row}
                    document_data['student'] = student
                    document = Document.objects.create(**document_data)

                return render(request, 'bulk_upload_csv.html', {'message': 'Data uploaded successfully'})
        except IntegrityError as e:
            return render(request, 'bulk_upload_csv.html', {'error_message': f"Error uploading data: {e}"})

    return render(request, 'bulk_upload_csv.html', {'error_message': 'Invalid request'})