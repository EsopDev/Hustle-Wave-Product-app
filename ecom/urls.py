from django.urls import path
from .views import product_list, create_product, product_detail

urlpatterns = [
    path('', product_list, name='product_list'),
    path('create/', create_product, name='create_product'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
]