from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import*

from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

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
    return render(request,"admindash.html",{'alumni_data':Alumni.objects.all().values()})

def alumnidash(request):
    return render(request,"alumnidash.html")

def logout(request):
    return render(request,"index.html")


@require_POST
def add_alumni(request):
    """View to add alumni data and return messages."""

    print("Add Alumni")
    try:
        age = int(request.POST['age'])
        validate_email(request.POST['alumni_email'])
        Alumni.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            alumni_name=request.POST['alumni_name'],
            DOB=request.POST['DOB'],
            age=age,
            alumni_email=request.POST['alumni_email'],
            alumni_phone=request.POST['alumni_phone'],
            address=request.POST['address'],
            street_name=request.POST['street_name'],
            city=request.POST['city'],
            pincode=request.POST['pincode'],
        )
        alumni_list = Alumni.objects.all().values() 
        for alumni_data in alumni_list:
           print("Alumni Record:")
           for field, value in alumni_data.items():
              print(f"  {field}: {value}")
              print("-" * 20)
        return HttpResponse("Alumni added successfully!")

    except (ValueError, ValidationError) as e:
        return HttpResponse(f"Alumni addition failed: {e}")

    except Exception as e:
        return HttpResponse(f"An unexpected error occurred: {e}")
    
@require_POST
def add_event(request):
    """View to add event data and return messages."""

    print("Add Event")
    try:
        Event.objects.create(
            event_name=request.POST['event_name'],
            event_date=request.POST['event_date'],
            location=request.POST['location'],
        )
        event_list = Event.objects.all().values()
        for event_data in event_list:
            print("Event Record:")
            for field, value in event_data.items():
                print(f"  {field}: {value}")
            print("-" * 20)
        return HttpResponse("Event added successfully!")

    except Exception as e:
        return HttpResponse(f"Event addition failed: {e}")