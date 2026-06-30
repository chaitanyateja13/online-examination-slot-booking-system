import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User, Student
from academics.models import Course, StudentCourse
from exams.models import EvaluationAssignment

def seed_50_students():
    print("Seeding 50 students...")
    course = Course.objects.get(course_code='CS301')
    
    # We want roll numbers to start from STU1002 to STU1051
    # since student1 is STU1001.
    
    for i in range(2, 52):
        username = f"student{i}"
        roll_number = f"STU{1000+i}"
        
        # Create User
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, email=f"{username}@ems.com", password="student123", role="STUDENT")
            # Create Student Profile
            student = Student.objects.create(user=user, roll_number=roll_number, department='Computer Science', semester=6)
            
            # Enroll in Course
            StudentCourse.objects.get_or_create(student=student, course=course)
            
            print(f"Created and enrolled {username} ({roll_number})")
            
    # Also update the evaluation assignment to cover this entire range
    # The existing assignment was STU1000 to STU2000, so it should already cover STU1001 to STU1051.
    # Let's just confirm it exists.
    assignment = EvaluationAssignment.objects.first()
    if assignment:
        assignment.start_roll_number = 'STU1000'
        assignment.end_roll_number = 'STU2000'
        assignment.save()
        
    print("Successfully seeded 50 students!")

if __name__ == '__main__':
    seed_50_students()
