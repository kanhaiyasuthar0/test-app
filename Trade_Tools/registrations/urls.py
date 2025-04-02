from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'registration'  # Namespace defined here
urlpatterns = [
    path('sign_up/', views.sign_up, name='sign_up'),
    path('login/', views.login_view, name='login'),  # Home page route after successful login
]
