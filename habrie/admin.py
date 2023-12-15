from django.contrib import admin
from .models import Student, Parent, Document, AcademicDetails

admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Document)
admin.site.register(AcademicDetails)