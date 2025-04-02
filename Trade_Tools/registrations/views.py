from django.shortcuts import render, get_object_or_404,redirect
# from .forms import  userRegistrationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
import pdb
from django.contrib.auth.views import PasswordResetView

def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if the username already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken.")
            return redirect('registration:sign_up')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('registration:sign_up')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('registration:sign_up')

        # Creating user and logging them in directly
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Authenticate and log the user in automatically
        user = authenticate(request, username=username, password=password1)
        if user:
            login(request, user)  # This line logs the user in
            messages.success(request, "Account created successfully!")
            return redirect('trade_home')  # Redirecting to home page after login
    return render(request, 'registration/register.html')




def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            from django.contrib.auth.models import User
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return render(request, 'registration/login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password")
    return render(request, 'registration/login.html')



class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/custom_password_reset_email.html'


