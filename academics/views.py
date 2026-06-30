from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CourseSchedule, Attendance, StudentCourse
from datetime import date

@login_required
def mark_attendance(request, schedule_id):
    if request.user.role != 'FACULTY':
        return redirect('home')
        
    faculty = request.user.faculty_profile
    schedule = get_object_or_404(CourseSchedule, id=schedule_id, faculty=faculty)
    
    # Get all students enrolled in this course
    enrolled_students = StudentCourse.objects.filter(course=schedule.course).select_related('student', 'student__user')
    
    if request.method == 'POST':
        attendance_date_str = request.POST.get('attendance_date')
        if not attendance_date_str:
            messages.error(request, "Please provide a valid date.")
            return redirect('mark_attendance', schedule_id=schedule_id)
            
        attendance_date = date.fromisoformat(attendance_date_str)
        
        for enrollment in enrolled_students:
            student = enrollment.student
            status = request.POST.get(f'status_{student.id}', 'A')
            
            # Update or create attendance
            Attendance.objects.update_or_create(
                student=student,
                course_schedule=schedule,
                date=attendance_date,
                defaults={'status': status, 'marked_by': faculty}
            )
            
        messages.success(request, "Attendance marked successfully.")
        return redirect('faculty_dashboard')
        
    return render(request, 'academics/mark_attendance.html', {
        'schedule': schedule, 
        'enrolled_students': enrolled_students,
        'today': date.today().isoformat()
    })
