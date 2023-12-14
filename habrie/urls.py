from django.urls import path
from .views import add_student


urlpatterns = [
    path('add_students/',add_student, name='add_students')
]
