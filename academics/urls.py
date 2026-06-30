from django.urls import path
from . import views

urlpatterns = [
    path('schedule/<int:schedule_id>/attendance/', views.mark_attendance, name='mark_attendance'),
]
