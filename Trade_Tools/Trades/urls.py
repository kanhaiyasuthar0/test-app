from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('product/', product_list, name='product'),
    path('courses/', course_list, name='courses'),
    path('', trade_home ,name='trade_home'),  # Define specific path for trade_home
    path('download/<int:product_id>/', download_file, name='download_file'),
    path('initiate_payment_and_log/<int:product_id>/<int:price>/<str:title>/', initiate_payment_and_log, name='initiate_payment_and_log'),
    path('initiate_payment/', initiate_payment, name='initiate_payment'),
    path("my-payments/", user_payments, name="user_payments"),
    path('payment-success/', payment_success, name='payment_success'),
    path('product/add/', product_create_or_update, name='product_add'),
    path('product/edit/<int:pk>/', product_create_or_update, name='product_edit'),
    path('about_us/', about, name='about'),
    path('manage-coupons/', manage_coupons, name='manage_coupons')
]

