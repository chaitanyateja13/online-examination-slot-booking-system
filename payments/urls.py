from django.urls import path
from . import views

urlpatterns = [
    path('initiate/<int:semester>/', views.initiate_payment, name='initiate_payment'),
    path('gateway/<int:payment_id>/', views.mock_payment_gateway, name='mock_payment_gateway'),
]
