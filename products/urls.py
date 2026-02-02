from django.urls import path, include
from products.views.products import ProductsListView, ProductsDetailView
from products.views.categories import CategoriesView

urlpatterns = [
    path('products/', ProductsListView.as_view()),
    path('products/<int:id>/<slug:slug>/', ProductsDetailView.as_view()),
    path('categories/', CategoriesView.as_view()),
]