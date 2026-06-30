from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Payment
import uuid

@login_required
def initiate_payment(request, semester):
    if request.user.role != 'STUDENT':
        return redirect('home')
        
    student = request.user.student_profile
    payment, created = Payment.objects.get_or_create(
        student=student, 
        semester=semester,
        defaults={'amount': 50000.00, 'status': 'PENDING'}
    )
    
    if payment.status == 'PAID':
        messages.info(request, f"Fee for semester {semester} is already paid.")
        return redirect('student_dashboard')
        
    return render(request, 'payments/initiate.html', {'payment': payment})

@login_required
def mock_payment_gateway(request, payment_id):
    if request.user.role != 'STUDENT':
        return redirect('home')
        
    payment = get_object_or_404(Payment, id=payment_id, student=request.user.student_profile)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'success':
            payment.status = 'PAID'
            payment.transaction_id = str(uuid.uuid4())
            payment.payment_date = timezone.now()
            payment.save()
            messages.success(request, "Payment successful! Receipt generated.")
        else:
            payment.status = 'FAILED'
            payment.save()
            messages.error(request, "Payment failed. Please try again.")
            
        return redirect('student_dashboard')
        
    return render(request, 'payments/gateway.html', {'payment': payment})
