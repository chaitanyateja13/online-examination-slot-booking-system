from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification
from accounts.models import User

@login_required
def send_notification(request):
    if request.user.role != 'ADMIN':
        return redirect('home')
        
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        target_role = request.POST.get('target_role')
        
        # Determine targets
        if target_role == 'ALL':
            users = User.objects.exclude(id=request.user.id)
        else:
            users = User.objects.filter(role=target_role)
            
        # Create notifications in bulk
        notifications = [
            Notification(user=u, title=title, message=message, notification_type='SYSTEM')
            for u in users
        ]
        Notification.objects.bulk_create(notifications)
        
        messages.success(request, f"Notification sent to {users.count()} users.")
        return redirect('admin_dashboard')
        
    return render(request, 'admin/send_notification.html')
