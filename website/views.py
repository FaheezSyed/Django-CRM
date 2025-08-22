from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import records



# Create your views here.
def home(request):
    #checking if loggingn in
    rec = records.objects.all()
    
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
        return render(request, "home.html", {"records":rec})
    
def logout_user(request):
    logout(request)
    messages.success(request, "Logged Out!")
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration Successful!")
            return redirect('home')
        else:
            messages.error(request, "Registration Failed. Please correct the errors below.")
    else:
        form = SignUpForm()
    return render(request, "register.html", {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:

        customer_record = records.objects.get(id = pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.error(request, "Please Login")
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_item = records.objects.get(id=pk)
        delete_item.delete()
        messages.success(request, "record deleted successfully")
        return redirect('home')
    else:
        messages.error(request, "Please Login")
        return redirect('home')


        
def add_record(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            state = request.POST.get('state')
            city = request.POST.get('city')
            zipcode = request.POST.get('zipcode')

            new_record = records.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                state=state,
                city=city,
                zipcode=zipcode
            )
            messages.success(request, "Record added successfully!")
            return redirect('home')
        else:
            return render(request, 'add_record.html', {})
    else:
        messages.error(request, "Please Login")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = records.objects.get(id=pk)
        if request.method == "POST":
            current_record.first_name = request.POST.get('first_name')
            current_record.last_name = request.POST.get('last_name')
            current_record.email = request.POST.get('email')
            current_record.phone = request.POST.get('phone')
            current_record.address = request.POST.get('address')
            current_record.state = request.POST.get('state')
            current_record.city = request.POST.get('city')
            current_record.zipcode = request.POST.get('zipcode')
            current_record.save()
            messages.success(request, "Record updated successfully!")
            return redirect('record', pk=pk)
       