from django.urls import path
from .views import add_student, handle_uploaded_csv,StudentListView, ExportDataView


urlpatterns = [
    path('add_students/',add_student, name='add_students'),
    path('bulk_uploding/', handle_uploaded_csv, name='bulk_uploding'),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('export_data/', ExportDataView.as_view(), name='export_data'),

]
