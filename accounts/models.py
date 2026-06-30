from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('FACULTY', 'Faculty'),
        ('STUDENT', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} - {self.role}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    semester = models.IntegerField(default=1)
    current_cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.roll_number} - {self.user.get_full_name()}"

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"
