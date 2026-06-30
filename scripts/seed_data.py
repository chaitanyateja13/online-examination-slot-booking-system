import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User, Student, Faculty
from academics.models import Course, CourseSchedule, StudentCourse
from exams.models import Exam, Slot

def seed_data():
    print("Seeding database...")
    
    # 1. Create Admin
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@ems.com', 'admin123', role='ADMIN')
        print("Admin created (admin/admin123)")
        
    # 2. Create Faculty
    if not User.objects.filter(username='faculty1').exists():
        f_user = User.objects.create_user('faculty1', 'faculty1@ems.com', 'faculty123', role='FACULTY')
        f_profile = Faculty.objects.create(user=f_user, employee_id='FAC001', department='Computer Science')
        print("Faculty created (faculty1/faculty123)")
    else:
        f_profile = Faculty.objects.get(user__username='faculty1')

    # 3. Create Student
    if not User.objects.filter(username='student1').exists():
        s_user = User.objects.create_user('student1', 'student1@ems.com', 'student123', role='STUDENT')
        s_profile = Student.objects.create(user=s_user, roll_number='STU1001', department='Computer Science', semester=6)
        print("Student created (student1/student123)")
    else:
        s_profile = Student.objects.get(user__username='student1')

    # 4. Create Course & Schedule
    course, _ = Course.objects.get_or_create(course_code='CS301', name='Database Management Systems', credits=4, semester=6)
    CourseSchedule.objects.get_or_create(course=course, faculty=f_profile, day_of_week='MON', start_time='10:00:00', end_time='11:30:00', room='402')
    
    # Enroll Student
    StudentCourse.objects.get_or_create(student=s_profile, course=course)

    # 5. Create Exam & Slot
    exam, _ = Exam.objects.get_or_create(course=course, name='DBMS Midterm', exam_type='REGULAR', total_marks=100, passing_marks=40)
    Slot.objects.get_or_create(exam=exam, date='2026-12-15', start_time='10:00:00', end_time='13:00:00', room='Hall A', capacity=50, available_seats=50, status='OPEN')

    print("Seed data completed successfully!")

if __name__ == '__main__':
    seed_data()
