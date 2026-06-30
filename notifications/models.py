from django.db import models
from accounts.models import User

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('BOOKING', 'Booking Confirmation'),
        ('EXAM_REMINDER', 'Exam Reminder'),
        ('RESULT', 'Result Declaration'),
        ('ATTENDANCE', 'Attendance Shortage'),
        ('SYSTEM', 'System Alert'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='SYSTEM')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.notification_type} - {self.subject}"
