from django.db import models
from accounts.models import Student, Faculty

class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    credits = models.IntegerField(default=3)
    semester = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.course_code} - {self.name}"

class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_students')
    enrolled_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.roll_number} enrolled in {self.course.course_code}"

class CourseSchedule(models.Model):
    DAY_CHOICES = (
        ('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'),
        ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday')
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedules')
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='teaching_schedules')
    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.course.course_code} - {self.day_of_week} {self.start_time}"

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    course_schedule = models.ForeignKey(CourseSchedule, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    marked_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course_schedule', 'date')

    def __str__(self):
        return f"{self.student.roll_number} - {self.course_schedule.course.course_code} - {self.date} - {self.status}"
