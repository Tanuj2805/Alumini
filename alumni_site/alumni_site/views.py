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

        print("User Email = ",email)
        print("User Password = ",password)

        # Try login with admin/staff model first
        try:
            user = Login.objects.get(email=email)
            if check_password(password, user.password) or password == user.password:
                messages.success(request, "Admin login successful!")
                return redirect("admindash")
            else:
                messages.error(request, "Invalid password")
        except Login.DoesNotExist:
            # If not found in Login model, try Alumni model
            try:
                alumni = Alumni.objects.get(alumni_email=email)
                if check_password(password, alumni.password) or password == alumni.password:
                    # You can set session here if needed
                    request.session["alumni_id"] = str(alumni._id)
                    request.session["alumni_email"] = str(alumni.alumni_email)
                    request.session["alumni_name"] = str(alumni.alumni_name)

                    # print alumni logged in
                    print("Current User = ",request.session.get('alumni_name'))

                    messages.success(request, "Alumni login successful!")
                    return redirect("alumnidash")
                else:
                    messages.error(request, "Invalid password")
            except Alumni.DoesNotExist:
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
    jobs = Job.objects.all()
    events = Event.objects.all().order_by('event_date')
    print(events)
    upcoming_events = events.filter(event_date__gte=datetime.now().date())[:5]

    # Donations
    donations = Donation.objects.all()
    total_donations = donations.aggregate(total=Sum('amount'))['total'] or 0
    recent_donations = donations.order_by('-date')[:5]

    print("Total Alumni:",Alumni.objects.count())
    print("Total Events:",events.count())
    print("Total Job Postings:",Job.objects.count())

    context = {
        'alumni_data': alumni_queryset,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_alumni': Alumni.objects.count(),
        'total_job':Job.objects.count(),
        'jobs': jobs,
        'upcoming_events': events,
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

    posts = Post.objects.select_related('author').order_by('-created_at')
    alumni_name = request.session.get('alumni_name')
    print("Current Alumni = ",alumni_name)

    print("Type of Posts = ",type(posts))
    
    for post in posts:
        print("Image URL     =", post.image.url if post.image else "No Image")
        post_path = post.image.url 
        cleaned_path = post_path.replace("static/", "", 1)
        print(cleaned_path)

        print("Author ID     =", post.author._id)  # If you want to print alumni ID
        print("Author Name   =", post.author.alumni_name)
        print("Content       =", post.content)
        print("Image URL     =", post.image.url if post.image else "No Image")
        print("Image     =", post_path)
        print("Created At    =", post.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        print("-" * 40)

    context = {
        'account_holder':post.author,
        'alumni_name':alumni_name,
        'posts':posts
    }

    print(context)

    return render(request,"alumnidash.html",context)

def logout(request):
    return render(request,"index.html")

@require_POST
def add_alumni(request):
    try:
        # Retrieve POST data from the form
        avatar = request.FILES.get('avatar')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        alumni_name = request.POST.get('alumni_name')
        dob = request.POST.get('DOB')
        age = request.POST.get('age')
        alumni_email = request.POST.get('alumni_email')
        password = request.POST.get('alumni_email')
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
            password=password,
            alumni_phone=alumni_phone,
            address=full_address,
            department=department,
            graduation_year=graduation_year,
            created_at=now(),
            updated_at=now(),
            avatar=avatar
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
        print(name)
        event = Event.objects.get(event_name=name)
        print("deleted event ",event)
        # Delete the event
        event.delete()
        return redirect('admindash')

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

@require_POST
def add_job(request):
    try:
        # Extract POST fields
        position = request.POST.get('position')
        company = request.POST.get('company')
        location = request.POST.get('location')
        job_type = request.POST.get('job_type')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        salary = request.POST.get('salary', '')
        application_deadline = request.POST.get('application_deadline')
        contact_email = request.POST.get('contact_email')
        status = request.POST.get('status', 'draft')
        skills = [skill.strip() for skill in request.POST.get('skills_required', '').split(',') if skill.strip()]

        # Basic validation
        if not all([position, company, location, job_type, description, requirements, application_deadline, contact_email]):
            return JsonResponse({'success': False, 'message': 'All fields are required.'})

        # Handle salary parsing (e.g., "30000 - 50000")
        salary_range = {}
        if '-' in salary:
            parts = salary.split('-')
            if len(parts) == 2:
                salary_range = {
                    'min': parts[0].strip(),
                    'max': parts[1].strip()
                }

        # Create job object
        job = Job.objects.create(
            position=position,
            company=company,
            location=location,
            job_type=job_type,
            description=description,
            requirements=requirements,
            salary_range=salary_range,
            skills_required=skills,
            application_deadline=application_deadline,
            contact_email=contact_email,
            status=status,
            posted_date=datetime.now()
        )

        return JsonResponse({'success': True, 'message': 'Job posted successfully!', 'job_id': str(job._id)})

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})



@require_POST
def add_post(request):
    try:
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        status = request.POST.get('status')

        # Save post to the database
        Post.objects.create(
            title=title,
            content=content,
            category=category,
            status=status,
            author=request.user,
            created_date=datetime.now()
        )

        return JsonResponse({
            'success': True,
            'message': 'Post created successfully!'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"Post creation failed: {str(e)}"
        }, status=500)


@require_POST
def delete_job(request):
    try:
        job_id = request.POST.get('job_id')
        position = request.POST.get('position')
        company = request.POST.get('company')
        print("Job ID to delete:", job_id)

        job = Job.objects.filter(position=position, company=company).first()
        print("Job to delete:", job)

        if job:
            job.delete()
            return redirect('admindash')  # or replace with your job dashboard view
        else:
            return JsonResponse({
                'success': False,
                'message': 'Job not found'
            }, status=404)

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
    return redirect("admindash")

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
    return redirect("admindash")

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
    return redirect("admindash")

@require_POST
def edit_admin(request):
    return redirect("admindash")

@require_POST
def delete_admin(request):
    return redirect("admindash")

@login_required
@require_POST
def get_admin_details(request):
    return redirect("admindash")

@login_required
@require_POST
def get_job_details(request):
    return redirect("admindash")

@require_POST
def update_alumni_profile(request):
    if request.method == 'POST':
        return redirect('alumnidash')
    
@require_POST
def create_post(request):
    content = request.POST.get('content')
    image = request.FILES.get('image')

    print(content)

    # Get the current logged-in user's Alumni object
    try:
        alumni = Alumni.objects.all().first()
        print(alumni)
    except Alumni.DoesNotExist:
        # Handle gracefully if Alumni is not found
        return redirect('alumnidash')  # or show error message

    # Create and save the post
    post = Post.objects.create(
        author=alumni,
        content=content,
        image=image
    )

    print("Post Uploaded Successfully : ",post)

    return redirect('alumnidash')