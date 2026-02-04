from django.urls import path
from payments.views.orders import OrderCreateView

urlpatterns = [
    path('orders/', OrderCreateView.as_view()),
]