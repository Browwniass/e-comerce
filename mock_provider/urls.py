from django.urls import path

from mock_provider.views import MockGatewayPayView, MockGatewayCreateView

urlpatterns = [
    path('mock-gateway/', MockGatewayCreateView.as_view()),
    path('mock-gateway/<str:external_id>/', MockGatewayPayView.as_view()),
]