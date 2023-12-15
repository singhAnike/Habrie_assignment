from django.urls import path
from .views import add_student, handle_uploaded_csv


urlpatterns = [
    path('add_students/',add_student, name='add_students'),
    path('bulk_uploding/', handle_uploaded_csv, name='bulk_uploding'),

]
