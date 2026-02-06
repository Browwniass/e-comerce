from django.urls import path, include
from carts.views.carts import CartsView
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register(r"carts", CartsView)

urlpatterns = [
    path(r"", include(router.urls)),
]
