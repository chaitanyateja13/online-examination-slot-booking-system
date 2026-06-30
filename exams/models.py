from django.db import models
from accounts.models import Student, Faculty
from academics.models import Course

class Exam(models.Model):
    EXAM_TYPE_CHOICES = (
        ('REGULAR', 'Regular'),
        ('SUPPLEMENTARY', 'Supplementary'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    name = models.CharField(max_length=200) # e.g. Midterm, Final Semester
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES, default='REGULAR')
    total_marks = models.IntegerField(default=100)
    passing_marks = models.IntegerField(default=40)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.course_code} - {self.name} ({self.exam_type})"

class Slot(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
        ('CANCELLED', 'Cancelled'),
    )
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50)
    capacity = models.IntegerField(default=50)
    available_seats = models.IntegerField(default=50)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')

    def __str__(self):
        return f"{self.exam.name} - {self.date} {self.start_time} (Room {self.room})"

class StudentSlotBooking(models.Model):
    STATUS_CHOICES = (
        ('CONFIRMED', 'Confirmed'),
        ('WAITLISTED', 'Waitlisted'),
        ('CANCELLED', 'Cancelled'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='bookings')
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='CONFIRMED')
    booking_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'slot')

    def __str__(self):
        return f"{self.student.roll_number} - {self.slot} - {self.status}"

class EvaluationAssignment(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='evaluation_assignments')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='evaluation_assignments')
    start_roll_number = models.CharField(max_length=20)
    end_roll_number = models.CharField(max_length=20)
    assigned_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.faculty.employee_id} -> {self.exam.name} ({self.start_roll_number} to {self.end_roll_number})"

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    internal_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    external_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grade = models.CharField(max_length=5, blank=True, null=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    is_pass = models.BooleanField(default=False)
    attempt_number = models.IntegerField(default=1)
    evaluated_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='evaluated_results')
    declared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'exam', 'attempt_number')

    def save(self, *args, **kwargs):
        self.total_marks = self.internal_marks + self.external_marks
        self.is_pass = self.total_marks >= self.exam.passing_marks
        # Basic grading logic
        if self.total_marks >= 90: self.grade = 'O'
        elif self.total_marks >= 80: self.grade = 'A+'
        elif self.total_marks >= 70: self.grade = 'A'
        elif self.total_marks >= 60: self.grade = 'B+'
        elif self.total_marks >= 50: self.grade = 'B'
        elif self.total_marks >= 40: self.grade = 'C'
        else: self.grade = 'F'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.roll_number} - {self.exam.name} - {self.total_marks}"
