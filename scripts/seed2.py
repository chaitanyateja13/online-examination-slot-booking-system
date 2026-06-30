import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from exams.models import Exam, EvaluationAssignment
from accounts.models import Faculty

f = Faculty.objects.first()
e = Exam.objects.first()

if f and e:
    EvaluationAssignment.objects.get_or_create(faculty=f, exam=e, start_roll_number='STU1000', end_roll_number='STU2000')
    print("Seeded evaluation assignment.")
