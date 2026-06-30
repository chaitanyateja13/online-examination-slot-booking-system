from django.urls import path
from . import views

urlpatterns = [
    path('available/', views.available_exams, name='available_exams'),
    path('exam/<int:exam_id>/slots/', views.view_slots, name='view_slots'),
    path('slot/<int:slot_id>/book/', views.book_slot, name='book_slot'),
    path('evaluate/<int:assignment_id>/', views.evaluate_exam, name='evaluate_exam'),
    path('admin/slot/create/', views.create_exam_slot, name='create_exam_slot'),
    path('admin/auto-assign/', views.auto_assign_evaluators, name='auto_assign_evaluators'),
    path('hallticket/<int:booking_id>/', views.download_hallticket, name='download_hallticket'),
    path('student/results/', views.student_results, name='student_results'),
]
