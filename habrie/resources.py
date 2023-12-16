from import_export import resources
from .models import Student

class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = (
            'name', 'gender', 'adhar_card_number', 'dob', 'identification_marks',
            'admission_category', 'height', 'weight', 'mail_id', 'contact_detail',
            'address', 'parent__father_name', 'parent__father_qualification',
            'parent__father_profession', 'parent__father_designation',
            'parent__father_aadhar_card', 'parent__father_mobile_number',
            'parent__father_mail_id', 'parent__mother_name', 'parent__mother_qualification',
            'parent__mother_profession', 'parent__mother_designation',
            'parent__mother_aadhar_card', 'parent__mother_mobile_number',
            'parent__mother_mail_id', 'academic_details__enrollment_id',
            'academic_details__class_name', 'academic_details__section',
            'academic_details__date_of_joining',
            'documents__file', 'documents__document_type'
        )
