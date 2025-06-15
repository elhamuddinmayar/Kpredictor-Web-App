from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from .forms import UserRegistrationForm
from django.contrib.auth.models import  User

def welcome(request):
    return render(request, 'first.html')

def second(request):
    return render(request, 'second.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
            user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # return render(request,'account/register_done.html',{'new_user': new_user})
            messages.success(request, 'Successfully Registered')
            return redirect("login")
    else:
        user_form = UserRegistrationForm()
    return render(request,'registration/register.html',{'user_form': user_form})



def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        # Try to find the user by email
        try:
            user_obj = User.objects.get(email=identifier)
            username = user_obj.username
        except User.DoesNotExist:
            username = identifier  # Assume it's a username

        # Authenticate
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # <- Make sure 'home' route exists in your urls.py
        else:
            messages.error(request, 'Invalid username/email or password.')

    return render(request, 'registration/login.html')  # <- Ensure this template exists and is correct


def log_out_view(request):
    logout(request)
    return redirect("login")