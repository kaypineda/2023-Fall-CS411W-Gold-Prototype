from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomUserForm

# Create your views here.
def dashboard(request):
    return render(request, 'AppUser/dashboard.html')

def user_login(request):
    """
    Authenticates user login information. If user username and password
    cannot be authenticated, an error message appears. Otherwise the user
    is redirected to their dashboard.

    Parameters:
        request: requested object

    Returns:
        Login page
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)
        user = authenticate(request, username=email, password=password)
        print(user)
        
        if user is not None:
            login(request, user)
            return redirect('AppUser:dashboard')
        else:
            messages.success(request, ('There was an error logging in. Please try again.'))
            return redirect('AppUser:login')
        
    return render(request, 'AppUser/login.html')

def user_register(request):
    """
    Saves user registration information.

    Parameters:
        request: HTTP request object

    Returns:
        Register form
    """
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('AppUser:user_login')
    else:
        form = CustomUserForm()
    return render(request, 'AppUser/registerform.html', {'form': form})