from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('create/', views.create_product, name='create_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('signup', views.register_view, name='register'),
    path('settings/', views.settings_view, name='settings'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('confirm-payment/', views.confirm_payment, name='confirm_payment'),
    path('payment-history/', views.payment_history, name='payment_history'),
    path('admin-payments/', views.admin_payments, name='admin_payments'),
]
