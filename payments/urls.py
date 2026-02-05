from django.urls import path
from payments.views.orders import OrderCreateView
from payments.views.payments import PaymentCreateView, PaymentWebhookView

urlpatterns = [
    path('orders/', OrderCreateView.as_view()),
    path('payments/', PaymentCreateView.as_view()),
    path('payments/webhook/', PaymentWebhookView.as_view()),
]