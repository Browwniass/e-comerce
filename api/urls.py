from django.urls import path, include

from users.urls import urlpatterns as users_urls
from products.urls import urlpatterns as products_urls
from carts.urls import urlpatterns as carts_urls
from payments.urls import urlpatterns as payments_urls
from mock_provider.urls import urlpatterns as mock_provider_urls

app_name = "api"

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("auth/", include("djoser.social.urls")),
    path('oauth/', include('social_django.urls')),
]

urlpatterns += users_urls
urlpatterns += products_urls
urlpatterns += carts_urls
urlpatterns += payments_urls
urlpatterns += mock_provider_urls