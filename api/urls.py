from django.urls import path, include
from users.urls import urlpatterns as users_urls
app_name = 'api'

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += users_urls