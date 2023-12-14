from django.shortcuts import render, redirect
from .forms import StudentForm, ParentForm, AcademicDetailsForm, DocumentForm
from django.db import transaction

def add_student(request):
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

            return redirect('success_page')  # Redirect to a success page
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
    })

def generate_enrollment_id(student):
    # Implement your logic to generate enrollment ID
    # This is just a placeholder, adjust it based on your requirements
    return f"{student.dob.strftime('%d%m%y')}{student.name[:3].upper()}{randint(1, 999):03}"
