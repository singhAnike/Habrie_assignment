from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    adhar_card_number = models.CharField(max_length=20)
    dob = models.DateField()
    identification_marks = models.TextField()
    admission_category = models.CharField(max_length=50)
    height = models.FloatField()
    weight = models.FloatField()
    mail_id = models.EmailField()
    contact_detail = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name


class Parent(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='parent')
    father_name = models.CharField(max_length=255)
    father_qualification = models.CharField(max_length=100)
    father_profession = models.CharField(max_length=100)
    father_designation = models.CharField(max_length=100)
    father_aadhar_card = models.CharField(max_length=20)
    father_mobile_number = models.CharField(max_length=15)
    father_mail_id = models.EmailField()
    
    mother_name = models.CharField(max_length=255)
    mother_qualification = models.CharField(max_length=100)
    mother_profession = models.CharField(max_length=100)
    mother_designation = models.CharField(max_length=100)
    mother_aadhar_card = models.CharField(max_length=20)
    mother_mobile_number = models.CharField(max_length=15)
    mother_mail_id = models.EmailField()

    def __str__(self):
        return self.student.name


class AcademicDetails(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='academic_details')
    enrollment_id = models.CharField(max_length=12, unique=True)
    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=10)
    date_of_joining = models.DateField()

    def __str__(self):
        return f"{self.student.name} - {self.enrollment_id}"


class Document(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/')
    document_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.student.name} - {self.document_type}"
