from .models import Result

def generate_result(student, exam, internal_marks, external_marks, faculty):
    # Check if a result already exists for this exam
    result = Result.objects.filter(student=student, exam=exam).order_by('-attempt_number').first()
    
    if result:
        result.internal_marks = internal_marks
        result.external_marks = external_marks
        result.evaluated_by = faculty
        result.save()
    else:
        result = Result.objects.create(
            student=student,
            exam=exam,
            internal_marks=internal_marks,
            external_marks=external_marks,
            attempt_number=1,
            evaluated_by=faculty
        )
    # Total, pass/fail and grade logic is in Result.save()
    
    # Calculate GPA (simple logic: Grade Points * Credits)
    grade_points = {
        'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'C': 5, 'F': 0
    }
    points = grade_points.get(result.grade, 0)
    result.gpa = points # Keeping it simple for demo
    result.save(update_fields=['gpa'])
    return result

def calculate_cgpa(student):
    results = Result.objects.filter(student=student, is_pass=True)
    if not results.exists():
        return 0.0
    total_gpa = sum(r.gpa for r in results)
    cgpa = total_gpa / results.count()
    
    student.current_cgpa = cgpa
    student.save(update_fields=['current_cgpa'])
    return cgpa
