from django.urls import path, include
from products.views.products import ProductsListView, ProductsDetailView, ProductsCategoryView
from products.views.categories import CategoriesView
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register(r'categories', CategoriesView)

categories_router = routers.NestedSimpleRouter(router, r'categories', lookup='categories')
categories_router.register(r'products', ProductsCategoryView, basename='category-projects')

urlpatterns = [
    path('products/', ProductsListView.as_view()),
    path('products/<int:id>/<slug:slug>/', ProductsDetailView.as_view()),
    #path('categories/<slug:slug>/', CategoriesView.as_view()),
    path(r'', include(router.urls)),
    path(r'', include(categories_router.urls)),
]