from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList.as_view(), name='product_list'),
    path('category/<slug:slug>/', ProductListByCategory.as_view(), name='product_list_by_category'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product_detail')
]
