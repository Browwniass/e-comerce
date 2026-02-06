from django.urls import path
from users.views.users import LogoutView
from users.views.users import GoogleLoginView

urlpatterns = [
    path("logout/", LogoutView.as_view(), name="logout"),
    path("auth/google/", GoogleLoginView.as_view(), name="google-login"),
]
