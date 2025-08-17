from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.
def home(request):
    #checking if loggingn in
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        
        #Authentication
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been Logged in!")
            return redirect('home')
        
        else:
            messages.success(request, "There is an error Loging In, Please check your credentials!")
            return redirect('home')
    else:
        return render(request, "home.html", {})
    
def logout_user(request):
    logout(request)
    messages.success(request, "Logged Out!")
    return redirect('home')
