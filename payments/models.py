from django.db import models
from accounts.models import Student

class Payment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    semester = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.roll_number} - Sem {self.semester} - {self.status}"
