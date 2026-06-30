import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from academics.models import Course, StudentCourse, CourseSchedule
from exams.models import Exam, Slot
from accounts.models import Student, Faculty

def run():
    print("Creating second course and exam...")
    c, _ = Course.objects.get_or_create(course_code='SE302', defaults={'name': 'Software Engineering', 'semester': 6, 'credits': 4})
    
    s1 = Student.objects.get(user__username='student1')
    StudentCourse.objects.get_or_create(student=s1, course=c)
    
    f = Faculty.objects.first()
    CourseSchedule.objects.get_or_create(course=c, faculty=f, defaults={'day_of_week': 'TUE', 'start_time': '10:00:00', 'end_time': '11:00:00', 'room': 'Room 102'})
    
    exam, _ = Exam.objects.get_or_create(course=c, name='SE Midterm', defaults={'exam_type': 'MIDTERM', 'total_marks': 100, 'passing_marks': 40})
    
    slot_date = timezone.now().date() + timedelta(days=15)
    Slot.objects.get_or_create(exam=exam, date=slot_date, defaults={'start_time': '14:00:00', 'end_time': '17:00:00', 'room': 'Hall C', 'capacity': 50, 'available_seats': 50, 'status': 'OPEN'})
    
    print("Added SE302 course, exam, and slot for student1.")

if __name__ == '__main__':
    run()
