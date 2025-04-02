from django.contrib import admin
from django.urls import path,include
from .views import *


urlpatterns = [
    path('', home_view, name='home'),
    path('product_list_admin/', product_list_admin, name='product_list_admin'),
    path('update-payment-status2/', update_payment_status2, name='update_payment_status2'),
    # path('dashboard/', dashboard, name='dashboard'),
    path('dj-admin/', dashboard_view ,name='dashboard' ),
    path('update-payment-status/', update_payment_status ,name='update_payment_status' )
]

