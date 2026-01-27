from django.urls import path
from users.views.users import LogoutView

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
]