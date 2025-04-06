from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import*
from django.db.models import Q, Sum, Count
from datetime import datetime, timedelta
from django.utils.timezone import now
import traceback

from django.views.decorators.http import require_POST, require_http_methods
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Job

def index(request):
    return render(request,"index.html")

def login(request):
    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")

        print(Login.objects.all())

        print(email,password)
        for user in Login.objects.all():
            print(f"Email: {user.email}, Name: {user.name}, Password: {user.password}")

        try:
            print("user","1")
            user = Login.objects.get(email=email)  # Check if user exists
            print(user,user.password)

            if check_password(password, user.password) or password == user.password:  # Check password (not secure, use hashing instead)
                messages.success(request, "Login successful!")
                print("Success")
                return redirect("admindash")  # Redirect to a homepage or dashboard
            else:
                messages.error(request, "Invalid password")
                print("Failed")
        except Login.DoesNotExist:
            messages.error(request, "User does not exist")

    return render(request, "login.html")

from django.shortcuts import render
from django.db.models import Q, Sum
from datetime import datetime
from .models import Alumni, Job, Event, Donation

def admindash(request):
    # Get query parameters for filtering and sorting
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '')

    # Get all alumni records from MongoDB
    alumni_queryset = Alumni.objects.all()

    # Apply search filter if provided
    if search_query:
        alumni_queryset = alumni_queryset.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(alumni_name__icontains=search_query) |
            Q(alumni_email__icontains=search_query) 
        )

    # Apply sorting if provided
    if sort_by == 'name':
        alumni_queryset = alumni_queryset.order_by('alumni_name')
    elif sort_by == 'email':
        alumni_queryset = alumni_queryset.order_by('alumni_email')
    elif sort_by == 'city':
        alumni_queryset = alumni_queryset.order_by('city')

    # Get jobs and events
    jobs = Job.objects.all().order_by('-posted_date')
    events = Event.objects.all().order_by('event_date')
    upcoming_events = events.filter(event_date__gte=datetime.now().date())[:5]

    # Donations
    donations = Donation.objects.all()
    total_donations = donations.aggregate(total=Sum('amount'))['total'] or 0
    recent_donations = donations.order_by('-date')[:5]

    context = {
        'alumni_data': alumni_queryset,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_alumni': alumni_queryset.count(),
        'jobs': jobs,
        'upcoming_events': upcoming_events,
        'total_events': events.count(),
        'total_donations': total_donations,
        'recent_donations': recent_donations,
        'engagement_rate': 78,  # Placeholder
        'alumni_growth_data': {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'data': [100, 120, 150, 180, 200, 250]
        },
        'event_participation_data': {
            'labels': ['Event 1', 'Event 2', 'Event 3', 'Event 4', 'Event 5'],
            'data': [65, 59, 80, 81, 56]
        }
    }

    return render(request, "admindash.html", context)


def alumnidash(request):
    return render(request,"alumnidash.html")

def logout(request):
    return render(request,"index.html")

@require_POST
def add_alumni(request):
    try:
        # Retrieve POST data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        alumni_name = request.POST.get('alumni_name')
        dob = request.POST.get('DOB')
        age = request.POST.get('age')
        alumni_email = request.POST.get('alumni_email')
        alumni_phone = request.POST.get('alumni_phone')
        full_address = request.POST.get('full_address')
        street_name = request.POST.get('street_name')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        department = request.POST.get('department')
        graduation_year = request.POST.get('graduation_year')

        # Print the received data for debugging
        print("---- Alumni Form Data ----")
        print("First Name:", first_name)
        print("Last Name:", last_name)
        print("Full Name:", alumni_name)
        print("DOB:", dob)
        print("Age:", age)
        print("Email:", alumni_email)
        print("Phone:", alumni_phone)
        print("Full Address:", full_address)
        print("Street Name:", street_name)
        print("City:", city)
        print("Pincode:", pincode)
        print("Department:", department)
        print("Graduation Year:", graduation_year)
        print("---------------------------")

        alumni = Alumni.objects.create(
            first_name=first_name,
            last_name=last_name,
            alumni_name=alumni_name,
            DOB=dob,
            age=age,
            alumni_email=alumni_email,
            alumni_phone=alumni_phone,
            address=full_address,
            department=department,
            graduation_year=graduation_year,
            created_at=now(),
            updated_at=now()
        )

        print(alumni)

        # Dummy response for now
        return JsonResponse({
            'success': True,
            'message': 'Alumni Added successfully!'
        })

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f"Error: {str(e)}"
        }, status=400)
    
@require_POST
def add_event(request):
    print("Add Event")
    try:
        Event.objects.create(
            event_name=request.POST['event_name'],
            event_date=request.POST['event_date'],
            location=request.POST['location'],
            description=request.POST.get('description', ''),
            max_participants=request.POST.get('max_participants', 0),
            tags=request.POST.getlist('tags') if 'tags' in request.POST else []
        )
        event_list = Event.objects.all().values()
        for event_data in event_list:
            print("Event Record:")
            for field, value in event_data.items():
                print(f"  {field}: {value}")
            print("-" * 20)
        return JsonResponse({
            'success': True,
            'message': 'Event added successfully!'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"Event addition failed: {e}"
        })


@login_required
@require_http_methods(["POST"])
def update_alumni_profile(request):
    try:
        # Get the alumni instance for the current user
        alumni = Alumni.objects.get(alumni_email=request.user.email)
        
        # Update the alumni fields
        alumni.first_name = request.POST.get('first_name')
        alumni.last_name = request.POST.get('last_name')
        alumni.alumni_name = request.POST.get('alumni_name')
        alumni.DOB = request.POST.get('DOB')
        alumni.age = request.POST.get('age')
        alumni.alumni_phone = request.POST.get('alumni_phone')
        alumni.address = request.POST.get('address')
        alumni.street_name = request.POST.get('street_name')
        alumni.city = request.POST.get('city')
        alumni.pincode = request.POST.get('pincode')
        
        # Handle profile picture upload if provided
        if 'profile_picture' in request.FILES:
            alumni.profile_picture = request.FILES['profile_picture']
        
        # Save the changes
        alumni.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Profile updated successfully'
        })
        
    except Alumni.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Alumni profile not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Alumni

@require_POST
def edit_alumni(request):
    try:
        email = request.POST.get('alumni_email')
        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Email is required to update alumni.'
            }, status=400)

        alumni = Alumni.objects.get(alumni_email=email)

        # Update alumni fields
        alumni.first_name = request.POST.get('first_name', alumni.first_name)
        alumni.last_name = request.POST.get('last_name', alumni.last_name)
        alumni.alumni_name = request.POST.get('alumni_name', alumni.alumni_name)
        alumni.DOB = request.POST.get('DOB', alumni.DOB)
        
        # Optional: calculate age dynamically here if needed
        age_value = request.POST.get('age')
        if age_value:
            alumni.age = int(age_value)
        
        alumni.alumni_phone = request.POST.get('alumni_phone', alumni.alumni_phone)
        alumni.address = request.POST.get('address', alumni.address)
        alumni.street_name = request.POST.get('street_name', alumni.street_name)
        alumni.city = request.POST.get('city', alumni.city)
        alumni.pincode = request.POST.get('pincode', alumni.pincode)

        alumni.save()

        return JsonResponse({
            'success': True,
            'message': 'Alumni updated successfully'
        })

    except Alumni.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Alumni not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }, status=500)


@require_POST
def delete_alumni(request):
    try:
        email = request.POST.get('alumni_email')
        print("Email",email)

        alumni = Alumni.objects.filter(alumni_email=email).first()
        print("Record to Delete ",alumni)
        # Delete the alumni
        alumni.delete()
        
        return redirect('admindash')
        
    except Alumni.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Alumni not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@require_POST
def get_alumni_details(request):
    try:
        alumni_id = request.POST.get('_id')
        alumni = Alumni.objects.get(alumni_id=alumni_id)
        
        # Convert date to string format for JSON
        dob_str = alumni.DOB.strftime('%Y-%m-%d')
        
        return JsonResponse({
            'success': True,
            'alumni': {
                'alumni_id': alumni.alumni_id,
                'first_name': alumni.first_name,
                'last_name': alumni.last_name,
                'alumni_name': alumni.alumni_name,
                'DOB': dob_str,
                'age': alumni.age,
                'alumni_email': alumni.alumni_email,
                'alumni_phone': alumni.alumni_phone,
                'address': alumni.address,
                'street_name': alumni.street_name,
                'city': alumni.city,
                'pincode': alumni.pincode
            }
        })
        
    except Alumni.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Alumni not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

# Event Management Functions
@require_POST
def edit_event(request):
    try:
        event_id = request.POST.get('event_id')
        event = Event.objects.get(event_id=event_id)
        
        # Update event fields
        event.event_name = request.POST.get('event_name')
        event.event_date = request.POST.get('event_date')
        event.location = request.POST.get('location')
        
        # Save the changes
        event.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Event updated successfully'
        })
        
    except Event.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Event not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@require_POST
def delete_event(request):
    try:
        name = request.POST.get('event_name')
        event = Event.objects.get(event_name=name)
        
        # Delete the event
        event.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Event deleted successfully'
        })
        
    except Event.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Event not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@require_POST
def get_event_details(request):
    try:
        event_id = request.POST.get('event_id')
        event = Event.objects.get(event_id=event_id)
        
        # Convert date to string format for JSON
        event_date_str = event.event_date.strftime('%Y-%m-%d')
        
        return JsonResponse({
            'success': True,
            'event': {
                'event_id': event.event_id,
                'event_name': event.event_name,
                'event_date': event_date_str,
                'location': event.location
            }
        })
        
    except Event.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Event not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

# Career Management Functions
@require_POST
def add_job(request):
    try:
        # Assuming you have a Job model
        Job.objects.create(
            position=request.POST['position'],
            company=request.POST['company'],
            location=request.POST['location'],
            description=request.POST['description'],
            requirements=request.POST['requirements'],
            posted_date=datetime.now().date(),
            status='active'
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Job posted successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"Job posting failed: {e}"
        })

@require_POST
def edit_job(request):
    try:
        job_id = request.POST.get('job_id')
        # job = Job.objects.get(job_id=job_id)
        
        # Update job fields
        # job.position = request.POST.get('position')
        # job.company = request.POST.get('company')
        # job.location = request.POST.get('location')
        # job.description = request.POST.get('description')
        # job.requirements = request.POST.get('requirements')
        # job.status = request.POST.get('status')
        
        # Save the changes
        # job.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Job updated successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@require_POST
def delete_job(request):
    try:
        job_id = request.POST.get('job_id')
        # job = Job.objects.get(job_id=job_id)
        
        # Delete the job
        # job.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Job deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

# Post Management Functions
@require_POST
def add_post(request):
    try:
        # Assuming you have a Post model
        # Post.objects.create(
        #     title=request.POST['title'],
        #     content=request.POST['content'],
        #     author=request.user,
        #     created_date=datetime.now()
        # )
        
        return JsonResponse({
            'success': True,
            'message': 'Post created successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"Post creation failed: {e}"
        })

@require_POST
def edit_post(request):
    try:
        post_id = request.POST.get('post_id')
        # post = Post.objects.get(post_id=post_id)
        
        # Update post fields
        # post.title = request.POST.get('title')
        # post.content = request.POST.get('content')
        
        # Save the changes
        # post.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Post updated successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@require_POST
def delete_post(request):
    try:
        post_id = request.POST.get('post_id')
        # post = Post.objects.get(post_id=post_id)
        
        # Delete the post
        # post.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Post deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@require_POST
def get_post_details(request):
    try:
        post_id = request.POST.get('post_id')
        # Assuming you have a Post model
        # post = Post.objects.get(id=post_id)
        
        # For now, return a mock response
        return JsonResponse({
            'success': True,
            'post': {
                'post_id': post_id,
                'title': 'Sample Post Title',
                'content': 'Sample post content',
                'category': 'news',
                'status': 'published',
                'created_at': datetime.now().strftime('%Y-%m-%d'),
                'updated_at': datetime.now().strftime('%Y-%m-%d')
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

# Donation Management Functions
@require_POST
def add_donation(request):
    try:
        # Assuming you have a Donation model
        # Donation.objects.create(
        #     donor=request.POST['donor'],
        #     amount=request.POST['amount'],
        #     date=datetime.now().date(),
        #     payment_method=request.POST['payment_method'],
        #     status='completed'
        # )
        
        return JsonResponse({
            'success': True,
            'message': 'Donation recorded successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"Donation recording failed: {e}"
        })

@require_POST
def edit_donation(request):
    try:
        donation_id = request.POST.get('donation_id')
        # donation = Donation.objects.get(donation_id=donation_id)
        
        # Update donation fields
        # donation.donor = request.POST.get('donor')
        # donation.amount = request.POST.get('amount')
        # donation.payment_method = request.POST.get('payment_method')
        # donation.status = request.POST.get('status')
        
        # Save the changes
        # donation.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Donation updated successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@require_POST
def delete_donation(request):
    try:
        donation_id = request.POST.get('donation_id')
        donation = Donation.objects.get(donation_id=donation_id)
        
        # Delete the donation
        donation.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Donation deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@require_POST
def get_donation_details(request):
    try:
        donation_id = request.POST.get('donation_id')
        donation = Donation.objects.get(donation_id=donation_id)
        
        # Convert date to string format for JSON
        date_str = donation.date.strftime('%Y-%m-%d')
        
        return JsonResponse({
            'success': True,
            'donation': {
                'donation_id': donation.donation_id,
                'donor_name': donation.donor,
                'amount': float(donation.amount),
                'payment_method': donation.payment_method,
                'status': donation.status,
                'date': date_str,
                'notes': donation.notes if hasattr(donation, 'notes') else ''
            }
        })
        
    except Donation.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Donation not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@require_POST
def generate_receipt(request):
    try:
        donation_id = request.POST.get('donation_id')
        donation = Donation.objects.get(donation_id=donation_id)
        
        # Format the date
        formatted_date = donation.date.strftime('%B %d, %Y')
        
        # Format the amount with commas for thousands
        formatted_amount = "{:,.2f}".format(float(donation.amount))
        
        # Generate receipt HTML
        receipt_html = f"""
        <div class="receipt">
            <div class="receipt-header">
                <h2>Donation Receipt</h2>
                <p>Receipt No: {donation.donation_id}</p>
                <p>Date: {formatted_date}</p>
            </div>
            
            <div class="receipt-body">
                <p><strong>Received from:</strong> {donation.donor}</p>
                <p><strong>Amount:</strong> ${formatted_amount}</p>
                <p><strong>Payment Method:</strong> {donation.payment_method}</p>
                <p><strong>Status:</strong> {donation.status}</p>
                {f'<p><strong>Notes:</strong> {donation.notes}</p>' if donation.notes else ''}
            </div>
            
            <div class="receipt-footer">
                <p>Thank you for your generous donation!</p>
                <p>This receipt is computer generated and does not require a signature.</p>
                <p class="small">For tax purposes: Our organization is a registered non-profit.</p>
            </div>
        </div>
        """
        
        return JsonResponse({
            'success': True,
            'receipt_html': receipt_html,
            'donation': {
                'donation_id': donation.donation_id,
                'donor_name': donation.donor,
                'amount': formatted_amount,
                'date': formatted_date,
                'payment_method': donation.payment_method
            }
        })
        
    except Donation.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Donation not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

# Admin Management Functions
@require_POST
def add_admin(request):
    try:
        # Assuming you have a Login model for admin users
        Login.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            password=request.POST['password'],
            role='admin'
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Admin added successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"Admin addition failed: {e}"
        })

@require_POST
def edit_admin(request):
    try:
        admin_id = request.POST.get('admin_id')
        admin = Login.objects.get(id=admin_id)
        
        # Update admin fields
        admin.name = request.POST.get('name')
        admin.email = request.POST.get('email')
        
        # Only update password if provided
        if request.POST.get('password'):
            admin.password = request.POST.get('password')
        
        # Save the changes
        admin.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Admin updated successfully'
        })
        
    except Login.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Admin not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@require_POST
def delete_admin(request):
    try:
        admin_id = request.POST.get('admin_id')
        admin = Login.objects.get(id=admin_id)
        
        # Delete the admin
        admin.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Admin deleted successfully'
        })
        
    except Login.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Admin not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@login_required
@require_POST
def get_admin_details(request):
    try:
        admin_id = request.POST.get('admin_id')
        admin = Login.objects.get(id=admin_id)
        
        return JsonResponse({
            'success': True,
            'admin': {
                'id': admin.id,
                'name': admin.name,
                'email': admin.email,
                'role': admin.role if hasattr(admin, 'role') else 'admin'
            }
        })
    except Login.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Admin not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@login_required
@require_POST
def get_job_details(request):
    try:
        job_id = request.POST.get('job_id')
        job = Job.objects.get(id=job_id)
        
        return JsonResponse({
            'success': True,
            'job': {
                'id': job.id,
                'position': job.position,
                'company': job.company,
                'location': job.location,
                'job_type': job.job_type,
                'description': job.description,
                'requirements': job.requirements,
                'application_deadline': job.application_deadline.strftime('%Y-%m-%d') if job.application_deadline else None,
                'contact_email': job.contact_email,
                'status': job.status
            }
        })
    except Job.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Job not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)