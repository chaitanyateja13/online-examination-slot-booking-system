import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import Student
from academics.models import CourseSchedule, Attendance, StudentCourse
from exams.models import StudentSlotBooking

def run():
    print("Updating CGPAs...")
    students = Student.objects.all()
    for s in students:
        s.current_cgpa = round(random.uniform(7.5, 9.5), 2)
        s.save(update_fields=['current_cgpa'])
        
    print("Seeding Attendance Records...")
    # First, let's clear existing attendance to start fresh
    Attendance.objects.all().delete()
    
    schedules = CourseSchedule.objects.all()
    for student in students:
        # Generate random attendance between 75% and 90%
        target_percentage = random.randint(75, 90)
        
        # Determine total classes (say 20 for this example)
        total_classes = 20
        present_classes = int((target_percentage / 100) * total_classes)
        absent_classes = total_classes - present_classes
        
        # Distribute randomly across the first schedule
        if schedules.exists():
            schedule = schedules.first()
            statuses = ['P'] * present_classes + ['A'] * absent_classes
            random.shuffle(statuses)
            
            attendance_records = []
            for i, status in enumerate(statuses):
                # Just using a mock date for each class (from 1 to 20 days ago)
                from django.utils import timezone
                from datetime import timedelta
                date = timezone.now().date() - timedelta(days=i)
                attendance_records.append(
                    Attendance(student=student, course_schedule=schedule, date=date, status=status)
                )
            Attendance.objects.bulk_create(attendance_records)
            
    print("Done generating random CGPAs and Attendance.")
    
    # Let's check enrollments for student1
    s1 = Student.objects.get(user__username='student1')
    enrollments = StudentCourse.objects.filter(student=s1)
    print(f"student1 is enrolled in {enrollments.count()} courses.")
    for e in enrollments:
        print(f" - {e.course.name} (Semester {e.course.semester})")
        
    # Check slots booked by student1
    bookings = StudentSlotBooking.objects.filter(student=s1)
    print(f"student1 has {bookings.count()} bookings.")
    for b in bookings:
        print(f" - {b.slot.exam.name} ({b.status})")

if __name__ == '__main__':
    run()
