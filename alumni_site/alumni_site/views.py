from django.shortcuts import render, redirect
from django.contrib import messages
from .models import*

def index(request):
    return render(request,"index.html")

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = Login.objects.get(email=email)  # Check if user exists
            if user.password == password:  # Check password (not secure, use hashing instead)
                messages.success(request, "Login successful!")
                return redirect("home")  # Redirect to a homepage or dashboard
            else:
                messages.error(request, "Invalid password")
        except Login.DoesNotExist:
            messages.error(request, "User does not exist")

    return render(request, "login.html")