from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from .models import Exam, Slot, StudentSlotBooking
from academics.models import Attendance, CourseSchedule, StudentCourse
from payments.models import Payment

@login_required
def available_exams(request):
    if request.user.role != 'STUDENT':
        return redirect('home')
    
    student = request.user.student_profile
    # Get enrolled courses
    enrolled_courses = student.enrollments.values_list('course_id', flat=True)
    # Get upcoming exams for those courses
    exams = Exam.objects.filter(course_id__in=enrolled_courses)
    
    return render(request, 'exams/available_exams.html', {'exams': exams})

@login_required
def view_slots(request, exam_id):
    if request.user.role != 'STUDENT':
        return redirect('home')
        
    exam = get_object_or_404(Exam, id=exam_id)
    slots = Slot.objects.filter(exam=exam, status='OPEN')
    return render(request, 'exams/slots.html', {'exam': exam, 'slots': slots})

@login_required
@transaction.atomic
def book_slot(request, slot_id):
    if request.user.role != 'STUDENT':
        return redirect('home')
        
    student = request.user.student_profile
    slot = get_object_or_404(Slot, id=slot_id)
    exam = slot.exam
    course = exam.course
    
    # 1. Eligibility Check: Payment
    payment = Payment.objects.filter(student=student, semester=course.semester).order_by('-created_at').first()
    if not payment or payment.status != 'PAID':
        messages.error(request, "Eligibility Failed: Pending fee payment.")
        return redirect('view_slots', exam_id=exam.id)
        
    # 2. Eligibility Check: Attendance >= 75%
    # This is a simplified calculation: total present / total classes * 100
    schedules = CourseSchedule.objects.filter(course=course)
    total_classes = Attendance.objects.filter(student=student, course_schedule__in=schedules).count()
    if total_classes == 0:
        attendance_percentage = 100 # Assume 100% if no classes held yet
    else:
        present_classes = Attendance.objects.filter(student=student, course_schedule__in=schedules, status='P').count()
        attendance_percentage = (present_classes / total_classes) * 100
        
    if attendance_percentage < 75:
        messages.error(request, f"Eligibility Failed: Attendance is {attendance_percentage:.2f}%. Requires 75%.")
        return redirect('view_slots', exam_id=exam.id)

    # 3. Check if already booked an exam
    if StudentSlotBooking.objects.filter(student=student, slot__exam=exam).exists():
        messages.warning(request, "You have already booked a slot for this exam.")
        return redirect('student_dashboard')
        
    # 4. Transaction Safe Booking
    # Lock the slot row to prevent concurrent overbooking
    slot = Slot.objects.select_for_update().get(id=slot_id)
    
    if slot.available_seats > 0:
        # Book confirmed
        StudentSlotBooking.objects.create(student=student, slot=slot, status='CONFIRMED')
        slot.available_seats = F('available_seats') - 1
        slot.save(update_fields=['available_seats'])
        messages.success(request, "You have successfully booked. All the best for your exam!")
    else:
        # Waitlist logic
        StudentSlotBooking.objects.create(student=student, slot=slot, status='WAITLISTED')
        messages.warning(request, "Slot is full. You have been added to the waitlist.")
        
    return redirect('student_dashboard')

from .models import EvaluationAssignment, Result
from .utils import generate_result
from academics.models import StudentCourse

@login_required
def evaluate_exam(request, assignment_id):
    if request.user.role != 'FACULTY':
        return redirect('home')
        
    faculty = request.user.faculty_profile
    assignment = get_object_or_404(EvaluationAssignment, id=assignment_id, faculty=faculty)
    
    # Simple logic: find students enrolled in this course who have bookings for this exam
    # and whose roll number falls in the assignment range.
    # For demo purposes, we will just fetch enrolled students and filter by roll number alphabetically.
    enrolled = StudentCourse.objects.filter(course=assignment.exam.course).select_related('student', 'student__user')
    students_to_eval = [
        e.student for e in enrolled 
        if assignment.start_roll_number <= e.student.roll_number <= assignment.end_roll_number
    ]
    
    # Fetch existing results
    student_ids = [s.id for s in students_to_eval]
    results = Result.objects.filter(student_id__in=student_ids, exam=assignment.exam)
    result_dict = {r.student_id: r for r in results}
    
    students_data = []
    for student in students_to_eval:
        students_data.append({
            'student': student,
            'result': result_dict.get(student.id)
        })

    if request.method == 'POST':
        for item in students_data:
            student = item['student']
            internal_str = request.POST.get(f'internal_{student.id}')
            external_str = request.POST.get(f'external_{student.id}')
            if internal_str and external_str:
                generate_result(
                    student=student, 
                    exam=assignment.exam, 
                    internal_marks=float(internal_str), 
                    external_marks=float(external_str), 
                    faculty=faculty
                )
        messages.success(request, "Evaluation submitted successfully.")
        return redirect('faculty_dashboard')
        
    return render(request, 'exams/evaluate.html', {
        'assignment': assignment,
        'students_data': students_data
    })

@login_required
def create_exam_slot(request):
    if request.user.role != 'ADMIN':
        return redirect('home')
    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        room = request.POST.get('room')
        capacity = request.POST.get('capacity')
        
        exam = Exam.objects.get(id=exam_id)
        Slot.objects.create(
            exam=exam, date=date, start_time=start_time, end_time=end_time, 
            room=room, capacity=capacity, available_seats=capacity, status='OPEN'
        )
        messages.success(request, "Exam Slot created successfully.")
        return redirect('admin_dashboard')
        
    exams = Exam.objects.all()
    return render(request, 'admin/create_slot.html', {'exams': exams})

from accounts.models import Faculty
@login_required
def auto_assign_evaluators(request):
    if request.user.role != 'ADMIN':
        return redirect('home')
        
    if request.method == 'POST':
        # Simple auto-assign logic: grab the first exam and assign it to the first faculty
        # For a full implementation, you would distribute roll numbers evenly.
        faculty = Faculty.objects.first()
        exam = Exam.objects.first()
        if faculty and exam:
            EvaluationAssignment.objects.get_or_create(
                faculty=faculty, exam=exam, 
                defaults={'start_roll_number': 'STU1000', 'end_roll_number': 'STU3000'}
            )
            messages.success(request, f"Assigned {exam.name} evaluations to {faculty.user.username}.")
        else:
            messages.error(request, "Not enough data to auto-assign.")
        return redirect('admin_dashboard')
    
    # Just redirect back if GET
    return redirect('admin_dashboard')

@login_required
def download_hallticket(request, booking_id):
    if request.user.role != 'STUDENT':
        return redirect('home')
        
    student = request.user.student_profile
    booking = get_object_or_404(StudentSlotBooking, id=booking_id, student=student, status='CONFIRMED')
    
    return render(request, 'exams/hallticket.html', {'booking': booking, 'student': student})

@login_required
def student_results(request):
    if request.user.role != 'STUDENT':
        return redirect('home')
        
    student = request.user.student_profile
    results = Result.objects.filter(student=student)
    
    return render(request, 'exams/student_results.html', {
        'student': student,
        'results': results
    })
