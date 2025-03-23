from django.shortcuts import render, redirect
from django.contrib import messages
from .models import*

def index(request):
    return render(request,"index.html")

def login(request):
    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")

        print(email,password)

        try:
            
            user = Login.objects.get(email=email)  # Check if user exists
            print(user)
            if user.password == password:  # Check password (not secure, use hashing instead)
                messages.success(request, "Login successful!")
                print("Success")
                return redirect("admindash")  # Redirect to a homepage or dashboard
            else:
                messages.error(request, "Invalid password")
        except Login.DoesNotExist:
            messages.error(request, "User does not exist")
        
        for user in Login.objects.all():
            print(f"Email: {user.email}, Name: {user.name}, Password: {user.password}")

    return render(request, "login.html")

def admindash(request):
    return render(request,"admindash.html")