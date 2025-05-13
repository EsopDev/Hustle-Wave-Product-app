from django.urls import path
from .views import product_list, create_product

urlpatterns = [
    path('', product_list, name='product_list'),
    path('create/', create_product, name='create_product'),
]