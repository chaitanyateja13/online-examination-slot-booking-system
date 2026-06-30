from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home_redirect(request):
    if request.user.is_authenticated:
        if request.user.role == 'ADMIN':
            return redirect('admin_dashboard')
        elif request.user.role == 'FACULTY':
            return redirect('faculty_dashboard')
        return redirect('student_dashboard')
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', home_redirect, name='home'),
    path('exams/', include('exams.urls')),
    path('academics/', include('academics.urls')),
    path('notifications/', include('notifications.urls')),
    path('payments/', include('payments.urls')),
]
