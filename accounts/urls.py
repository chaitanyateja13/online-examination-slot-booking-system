from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/faculty/', views.faculty_dashboard, name='faculty_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('admin/users/', views.manage_users, name='manage_users'),
    path('admin/users/add/', views.add_student, name='add_student'),
    path('admin/users/remove/', views.remove_student, name='remove_student'),
    path('admin/users/faculty/add/', views.add_faculty, name='add_faculty'),
    path('admin/users/faculty/remove/', views.remove_faculty, name='remove_faculty'),
    path('admin/export-report/', views.export_report, name='export_report'),
]
