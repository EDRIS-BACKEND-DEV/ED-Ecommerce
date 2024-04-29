

from django.urls import path
# from .views import product_list, product_detail, ProductListView
from .views import ProductListView, ProductDetailView, AddProductFavorite


urlpatterns = [
    path('', ProductListView.as_view(), name='product_page'),
    path('cat/<cat>', ProductListView.as_view(), name='product-categories-list'),
    path('brand/<brand>', ProductListView.as_view(), name='product-by-brand'),
    path('product-favorite', AddProductFavorite.as_view(), name='product-favourite'),
    path('<slug:slug>', ProductDetailView.as_view() , name='product-detail'),
]
