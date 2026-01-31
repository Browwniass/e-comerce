from django.urls import path, include
from products.views.products import ProductsListView, ProductsDetailView

urlpatterns = [
    path('products/', ProductsListView.as_view()),
    path('products/<int:id>/<slug:slug>/', ProductsDetailView.as_view()),
]