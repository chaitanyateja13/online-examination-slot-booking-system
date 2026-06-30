from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from .forms import CustomLoginForm
from django.contrib.auth.decorators import login_required

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return reverse_lazy('admin_dashboard')
        elif user.role == 'FACULTY':
            return reverse_lazy('faculty_dashboard')
        elif user.role == 'STUDENT':
            return reverse_lazy('student_dashboard')
        return reverse_lazy('login')

def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard stubs to be implemented in phase 3
from accounts.models import Student, Faculty
from exams.models import Exam, Slot
from academics.models import Attendance
from django.db.models import Count, Q, Sum, F

@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        return redirect('home')

    total_students = Student.objects.count()
    total_faculty = Faculty.objects.count()
    exams_scheduled = Exam.objects.count()
    
    # Calculate exact attendance shortage dynamically
    attendance_shortage = 0
    all_students = Student.objects.all()
    for s in all_students:
        total_att = Attendance.objects.filter(student=s).count()
        if total_att > 0:
            present_att = Attendance.objects.filter(student=s, status='P').count()
            if (present_att / total_att) * 100 < 75:
                attendance_shortage += 1

    # Upcoming exams analytics
    # Fetch slots for analytics
    upcoming_exams = Exam.objects.annotate(
        total_capacity=Sum('slots__capacity'),
        booked_seats=Sum(F('slots__capacity') - F('slots__available_seats'))
    ).filter(slots__isnull=False).distinct()

    context = {
        'total_students': total_students,
        'total_faculty': total_faculty,
        'exams_scheduled': exams_scheduled,
        'attendance_shortage': attendance_shortage,
        'upcoming_exams': upcoming_exams,
    }
    return render(request, 'dashboard/admin.html', context)

from academics.models import CourseSchedule
from exams.models import EvaluationAssignment

def faculty_dashboard(request):
    faculty = request.user.faculty_profile
    schedules = CourseSchedule.objects.filter(faculty=faculty)
    evaluations = EvaluationAssignment.objects.filter(faculty=faculty)
    
    context = {
        'schedules': schedules,
        'evaluations': evaluations,
        'schedules_count': schedules.count(),
        'evaluations_count': evaluations.count()
    }
    return render(request, 'dashboard/faculty.html', context)

from exams.models import StudentSlotBooking
from notifications.models import Notification

@login_required
def student_dashboard(request):
    if request.user.role != 'STUDENT':
        return redirect('home')
        
    student = request.user.student_profile
    bookings = StudentSlotBooking.objects.filter(student=student).select_related('slot', 'slot__exam', 'slot__exam__course').order_by('slot__date')
    
    confirmed_count = bookings.filter(status='CONFIRMED').count()
    waitlist_count = bookings.filter(status='WAITLISTED').count()
    
    # Notifications for the student
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Fetch sample available exams for the dashboard if booking is empty
    enrolled_courses = student.enrollments.values_list('course_id', flat=True)
    available_exams_sample = Exam.objects.filter(course_id__in=enrolled_courses)[:2]
    
    # Fetch fee status
    from payments.models import Payment
    payment = Payment.objects.filter(student=student).order_by('-created_at').first()
    fee_status = payment.status if payment else 'PENDING'
    
    # Calculate Attendance Percentage
    from academics.models import Attendance
    total_attendance = Attendance.objects.filter(student=student).count()
    if total_attendance > 0:
        present = Attendance.objects.filter(student=student, status='P').count()
        attendance_percentage = int((present / total_attendance) * 100)
    else:
        attendance_percentage = 100
    
    context = {
        'bookings': bookings,
        'confirmed_count': confirmed_count,
        'waitlist_count': waitlist_count,
        'notifications': notifications,
        'available_exams_sample': available_exams_sample,
        'fee_status': fee_status,
        'attendance_percentage': attendance_percentage,
    }
    return render(request, 'dashboard/student.html', context)


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

from django.contrib.auth.hashers import make_password
from accounts.models import User, Student

@login_required
def manage_users(request):
    if request.user.role != 'ADMIN':
        return redirect('home')
    students = Student.objects.select_related('user').all()
    faculty = Faculty.objects.select_related('user').all()
    return render(request, 'admin/manage_users.html', {'students': students, 'faculty': faculty})

@login_required
def add_student(request):
    if request.user.role != 'ADMIN':
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        roll_number = request.POST.get('roll_number')
        department = request.POST.get('department')
        semester = request.POST.get('semester')
        
        # Simple validation
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, email=email, password='student123', role='STUDENT')
            Student.objects.create(user=user, roll_number=roll_number, department=department, semester=semester)
            # Add a message
        return redirect('manage_users')
        
    return render(request, 'admin/add_student.html')

from django.contrib import messages

@login_required
def remove_student(request):
    if request.user.role != 'ADMIN':
        return redirect('home')
        
    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        admin_password = request.POST.get('admin_password')
        
        # Verify admin password for security
        if not request.user.check_password(admin_password):
            messages.error(request, "Authentication failed. Invalid Admin Password.")
            return redirect('remove_student')
            
        try:
            student = Student.objects.get(roll_number=roll_number)
            user_to_delete = student.user
            # Delete user (this will cascade and delete student profile, bookings, results, etc)
            user_to_delete.delete()
            messages.success(request, f"Successfully removed student: {roll_number}")
            return redirect('manage_users')
        except Student.DoesNotExist:
            messages.error(request, "Student with this Roll Number does not exist.")
            return redirect('remove_student')
            
    return render(request, 'admin/remove_student.html')

@login_required
def add_faculty(request):
    if request.user.role != 'ADMIN':
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        employee_id = request.POST.get('employee_id')
        department = request.POST.get('department')
        designation = request.POST.get('designation')
        
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, email=email, password='faculty123', role='FACULTY')
            Faculty.objects.create(user=user, employee_id=employee_id, department=department, designation=designation)
            messages.success(request, f"Faculty {username} added successfully.")
        else:
            messages.error(request, "Username already exists.")
        return redirect('manage_users')
        
    return render(request, 'admin/add_faculty.html')

@login_required
def remove_faculty(request):
    if request.user.role != 'ADMIN':
        return redirect('home')
        
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        admin_password = request.POST.get('admin_password')
        
        if not request.user.check_password(admin_password):
            messages.error(request, "Authentication failed. Invalid Admin Password.")
            return redirect('remove_faculty')
            
        try:
            faculty = Faculty.objects.get(employee_id=employee_id)
            user_to_delete = faculty.user
            user_to_delete.delete()
            messages.success(request, f"Successfully removed faculty: {employee_id}")
            return redirect('manage_users')
        except Faculty.DoesNotExist:
            messages.error(request, "Faculty with this Employee ID does not exist.")
            return redirect('remove_faculty')
            
    return render(request, 'admin/remove_faculty.html')

import csv
from django.http import HttpResponse
from django.utils import timezone

@login_required
def export_report(request):
    if request.user.role != 'ADMIN':
        return redirect('home')
        
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="system_report_{timezone.now().date()}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Exam Name', 'Course', 'Total Capacity', 'Booked Seats', 'Status'])
    
    exams = Exam.objects.annotate(
        total_capacity=Sum('slots__capacity'),
        booked_seats=Sum(F('slots__capacity') - F('slots__available_seats'))
    ).filter(slots__isnull=False).distinct()
    
    for exam in exams:
        capacity = exam.total_capacity or 0
        booked = exam.booked_seats or 0
        status = 'Full' if capacity > 0 and booked >= capacity else 'Active'
        writer.writerow([exam.name, exam.course.course_code, capacity, booked, status])
        
    return response
