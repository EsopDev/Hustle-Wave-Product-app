from django.urls import path
from .views import product_list, create_product, product_detail, login_view, register_view, logout_view

urlpatterns = [
    path('', product_list, name='product_list'),
    path('create/', create_product, name='create_product'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('signup', register_view, name='register'),
]