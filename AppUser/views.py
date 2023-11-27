from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('AppUser:dashboard')
        else:
            messages.success(request, ('There was an error logging in. Please try again.'))
            return redirect('AppUser:login')
        
        return render(request, 'AppUser/login.html')