from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import*
from django.db.models import Q, Sum, Count
from datetime import datetime, timedelta
from django.utils.timezone import now
import traceback
from decimal import Decimal
from bson.decimal128 import Decimal128
from bson import ObjectId
import json
from django.core import serializers
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO

from django.views.decorators.http import require_POST, require_http_methods
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Job
from django.db.models import Sum, Count, Max

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
                request.session["admin_email"] = email
                return redirect("admindash")
            else:
                messages.error(request, "Invalid password")
        except Login.DoesNotExist:
            # If not found in Login model, try Alumni model
            try:
                alumni = Alumni.objects.get(alumni_email=email)

                print("-------------------------------------------------")
                print("After Login ID = ",alumni._id)
                print("-------------------------------------------------")
                if check_password(password, alumni.password) or password == alumni.password:
                    # You can set session here if needed
                    request.session["alumni_id"] = str(alumni._id)
                    request.session["alumni_email"] = str(alumni.alumni_email)
                    request.session["alumni_name"] = str(alumni.alumni_name)

                    # print alumni logged in
                    print("Current User = ",request.session.get('alumni_id'))
                    print("Current User = ",request.session.get('alumni_email'))
                    print("Current User = ",request.session.get('alumni_name'))

                    messages.success(request, "Alumni login successful!")
                    return redirect("alumnidash")
                else:
                    messages.error(request, "Invalid password")
            except Alumni.DoesNotExist:
                messages.error(request, "User does not exist")

    return render(request, "login.html")

def student_login(request):
    if request.method == 'POST':
        prn = request.POST.get('prn')
        password = request.POST.get('password')
        
        try:
            student = StudentLogin.objects.get(username=prn)
            if student.password == password:
                # Login successful - redirect to dashboard or homepage
                messages.success(request, f"Welcome {student.name}!")
                return redirect('studentdash')  # change as needed
            else:
                messages.error(request, "Invalid password.")
        except StudentLogin.DoesNotExist:
            messages.error(request, "Student with this PRN does not exist.")
    
    return render(request, 'student_login.html')

def studentdash(request):
    events = Event.objects.all().order_by('event_date')
    upcoming_events = events.filter(event_date__gte=datetime.now().date())[:5]
    
    # No need for select_related since Post no longer uses ForeignKey
    posts = Post.objects.all().order_by('-created_at')

    context = {
        'upcoming_events': upcoming_events,
        'posts': posts
    }
    return render(request, 'studentdash.html', context)

from django.shortcuts import render
from django.db.models import Q, Sum
from datetime import datetime, date
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
    invitations = EventInvitation.objects.select_related('event', 'alumni').all()
    
    donations = Donation.objects.all()
    total_donations = Decimal('0.0')
    recent_donations = []
    already_invited_ids = EventInvitation.objects.filter().values_list('alumni_id', flat=True)


    # Loop through all donations
    for d in sorted(donations, key=lambda x: x.date, reverse=True):
        # Convert amount if needed
        amt = d.amount
        if isinstance(amt, Decimal128):
            amt = amt.to_decimal()
        
        total_donations += amt  # Add to total

        # Get donor name from Alumni
        try:
            print('donor = ',d.donor_id)
            alumni = Alumni.objects.get(_id=d.donor_id)
            donor_name = alumni.alumni_name
            donor_email = alumni.alumni_email
        except Alumni.DoesNotExist:
            donor_name = "Unknown Donor"
            donor_email = "Unknown"

        # Add this donation to recent list (limit to 5)
        if len(recent_donations) < 5:
            recent_donations.append({
                'name': donor_name,
                'amount': amt,
                'date': d.date,
                'email':donor_email
            })

    print(recent_donations)
    # Final structure
    donation_stats = {
        'total_donations': total_donations,
        'recent_donations': recent_donations
    }

    print("Total Alumni:",Alumni.objects.count())
    print("Total Events:",events.count())
    print("Total Job Postings:",Job.objects.count())

    context = {
        'already_invited_ids': list(already_invited_ids),
        'upcoming_events': Event.objects.filter(event_date__gte=timezone.now()),
        'student_logins':StudentLogin.objects.all(),
        'invitations':invitations,
        'upcoming_events':upcoming_events,
        'posts':Post.objects.order_by('-created_at'),
        'donations':donations, 
        'alumni_data': alumni_queryset,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_alumni': Alumni.objects.count(),
        'total_job':Job.objects.count(),
        'jobs': jobs,
        'upcoming_events': events,
        'total_events': events.count(),
        'donation_stats': donation_stats,
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

    posts = Post.objects.order_by('-created_at')
    email = request.session.get('alumni_email')
    account_holder = Alumni.objects.filter(alumni_email=email).first()
    print("Account Holder = ",account_holder)
    self_posts = Post.objects.filter(author_email=email).order_by('-created_at')
    print(self_posts)

    print("-------------------------------------------------")
    # print("ID = ",account_holder._id)
    print("Avatar = ",account_holder.avatar)
    print("Avatar url = ",account_holder.avatar.url)
    print("Address = ",account_holder.address)
    print("Email = ",account_holder.alumni_email)
    print("Address = ",account_holder.alumni_phone)

    print("Type of Posts = ",type(posts))
    print("-------------------------------------------------")

    for post in posts:
        print("Image URL     =", post.image.url if post.image else "No Image")
        post_path = post.image.url 
        cleaned_path = post_path.replace("static/", "", 1)
        print(cleaned_path)

        print("Author ID     =", post.author_name)  # If you want to print alumni ID
        print("Author Name   =", post.author_email)
        print("Content       =", post.content)
        print("Image URL     =", post.image.url if post.image else "No Image")
        print("Image     =", post_path)
        print("Created At    =", post.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        print("-" * 40)
    print("-------------------------------------------------")
    
    invitations = EventInvitation.objects.all()
    today = timezone.now().date()    

    # invitations for events
    invitations = EventInvitation.objects.filter(
    alumni_id=ObjectId(account_holder.alumni_id()),
    status='pending').order_by('-sent_at')

    upcoming_events = EventInvitation.objects.filter()
    print("--------------------------------------------")
    print("Upcoming Events : ",upcoming_events)
    print("--------------------------------------------")

    upcoming_events = EventInvitation.objects.filter(alumni_id=ObjectId(account_holder.alumni_id()))
    print("--------------------------------------------")
    print("Upcoming Events : ",upcoming_events)
    print("--------------------------------------------")
    
    # Upcoming accepted events
    upcoming_events = EventInvitation.objects.filter(
        alumni_id=ObjectId(account_holder.alumni_id()),
        status='accepted',
        event__event_date__gte=today
    ).select_related('event').order_by('event__event_date')

    print("--------------------------------------------")
    print("Upcoming Events : ",upcoming_events)
    print("--------------------------------------------")
    
    # Past events (both accepted and declined)
    past_events = EventInvitation.objects.filter(
        alumni_id=ObjectId(account_holder.alumni_id()),
        event__event_date__lt=timezone.now().date()
    ).exclude(status='pending').select_related('event').order_by('-event__event_date')
    
    print("-----------------------------------------")
    print(invitations)


    #donation info for profile cards
    donations = Donation.objects.filter(donor=account_holder)
    print(donations)

    total_amount = Decimal('0.0')
    total_times = donations.count()
    latest_date = None

    for d in donations:
        amt = d.amount
        if isinstance(amt, Decimal128):
            amt = amt.to_decimal()
        total_amount += amt
        if not latest_date or d.date > latest_date:
            latest_date = d.date

    donation_stats = {
        'total_amount': total_amount,
        'total_times': total_times,
        'latest_date': latest_date
    }

    # Get latest donation details (if needed)
    latest = Donation.objects.filter(donor_id=account_holder._id).order_by('-date').first()

    # Store everything in one dictionary
    donation_data = {
        'total_donated': donation_stats['total_amount'] or 0,
        'donation_count': donation_stats['total_times'],
        'latest_donation': {
            'amount': latest.amount if latest else 0,
            'date': latest.date if latest else None,
            'method': latest.payment_method if latest else None,
            'notes': latest.notes if latest else ""
        }
    }

    print("-------------------------------------------------")
    print("Donation Data = ",donation_data)
    print("-------------------------------------------------")

    context = {
        'past_events':past_events,
        'upcoming_events':upcoming_events,
        'invitations':invitations,
        'donation_data':donation_data,
        'account_holder':account_holder,
        'posts':posts,
        'self_posts':self_posts
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
        alumni_name = request.POST.get('alumni_name')
        dob = request.POST.get('DOB')
        age = (date.today().year - datetime.strptime(request.POST.get('DOB'), '%Y-%m-%d').year) - (date.today() < datetime.strptime(request.POST.get('DOB'), '%Y-%m-%d').date().replace(year=date.today().year))
        alumni_email = request.POST.get('alumni_email')
        password = request.POST.get('alumni_email')
        alumni_phone = request.POST.get('alumni_phone')
        full_address = request.POST.get('full_address')
        department = request.POST.get('department')
        graduation_year = request.POST.get('graduation_year')

        # Print the received data for debugging
        print("---- Alumni Form Data ----")
        print("Full Name:", alumni_name)
        print("DOB:", dob)
        print("Age:", age)
        print("Email:", alumni_email)
        print("Phone:", alumni_phone)
        print("Full Address:", full_address)
        print("Department:", department)
        print("Graduation Year:", graduation_year)
        print("---------------------------")

        alumni = Alumni.objects.create(
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
def add_student(request):
    try:
        # Extract form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        dept = request.POST.get('dept')

        # Debug print
        print("---- Student Form Data ----")
        print("Username:", username)
        print("Password:", password)
        print("Name:", name)
        print("Department:", dept)
        print("----------------------------")

        # Optional: Validate numeric username
        if not username.isdigit():
            return JsonResponse({'success': False, 'message': 'Username must be numeric'}, status=400)

        student = StudentLogin.objects.create(
            username=int(username),
            password=password,  # Note: Hashing recommended
            name=name,
            dept=dept,
        )

        print("Created Student:", student)

        return redirect('admindash')
        return JsonResponse({
            'success': True,
            'message': 'Student added successfully!'
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


# @login_required
@require_POST
def update_alumni_profile(request):
    try:
        # Get the alumni instance for the current user
        alumni = Alumni.objects.filter(alumni_name=request.session.get('alumni_name')).first()
        
        print("-----------------------------------------------")
        print("Before:",alumni.alumni_name)

        # Update the alumni fields
        alumni.alumni_name = request.POST.get('alumni_name')
        alumni.alumni_phone = request.POST.get('alumni_phone')
        alumni.address = request.POST.get('address')

        print("After:",alumni.alumni_name)
        print("-----------------------------------------------")
 
        # Handle profile picture upload if provided
        if 'profile_picture' in request.FILES:
            alumni.avatar = request.FILES['profile_picture']
        
        # Save the changes
        alumni.save()
        return redirect('alumnidash')
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
def delete_student(request):
    username = request.POST.get('username')
    try:
        student = StudentLogin.objects.get(username=username)
        student.delete()
        return redirect('admindash')
        messages.success(request, "Student deleted successfully.")
    except StudentLogin.DoesNotExist:
        messages.error(request, "Student not found.")
    except Exception as e:
        messages.error(request, f"Error deleting student: {e}")
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

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
def send_event_invitations(request):
    try:
        data = json.loads(request.body)
        event_id = data.get('event_id')
        alumni_ids = data.get('alumni_ids', [])

        # Convert event_id and alumni_ids to ObjectId
        object_event_id = ObjectId(event_id)
        object_alumni_ids = [ObjectId(aid) for aid in alumni_ids]

        # Get event
        event = Event.objects.get(_id=object_event_id)

        # Get alumni objects
        alumni_to_invite = Alumni.objects.filter(_id__in=object_alumni_ids)

        # Create invitations
        for alumni in alumni_to_invite:
            EventInvitation.objects.get_or_create(
                event=event,
                alumni=alumni,
                defaults={'status': 'pending'}
            )

        # Add to many-to-many relationship
        event.invited_alumni.add(*alumni_to_invite)

        return JsonResponse({'success': True, 'message': 'Invitations sent successfully'})

    except Event.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Event not found'}, status=404)
    except Alumni.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'One or more alumni not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
def respond_to_invitation(request):
    try:
        invitation_id = request.POST.get('invitation_id')
        response = request.POST.get('response')

        if not invitation_id or response not in ['accepted', 'declined']:
            return redirect('alumnidash')  # fallback or error page

        # Get the EventInvitation object
        invitation = EventInvitation.objects.get(_id=ObjectId(invitation_id))

        # Update the invitation's status and timestamp
        invitation.status = response
        invitation.responded_at = timezone.now()
        invitation.save()

        return redirect('alumnidash')

    except EventInvitation.DoesNotExist:
        return redirect('alumnidash')

@require_POST
def delete_event(request):
    try:
        event_id = request.POST.get('event_id')
        print("Event ID received:", event_id)

        # Convert to ObjectId
        obj_id = ObjectId(event_id)

        # Get and delete the event
        event = Event.objects.get(_id=obj_id)
        print("Deleting event:", event.event_name)
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
        author_email = request.session.get('alumni_email')  # Verify your session key
        
        print("-----------------------------------------------")
        print("Email = ",author_email," Post ID = ",post_id)

        # Get author from session
        author = Alumni.objects.get(alumni_email=author_email)

        print("Alumni = ",author.alumni_name)
        
        # Find post by ID and author
        post = Post.objects.get(_id=ObjectId(post_id))
        post.delete()
        
        print("Delete Post Deleted")
        print("-----------------------------------------------")

        return redirect('alumnidash')

    except Post.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Post not found'}, status=404)
    except Exception as e:
        print("Error:", e)
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

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
def fake_payment(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        amount = request.POST.get('amount')
        notes = request.POST.get('notes')
        upi = request.POST.get('upi_id') or ''
        wallet = request.POST.get('wallet_number') or ''

        print("-------------------------------------")
        print("FAKE PAYMENT DONE...")
        print("-------------------------------------")

        if payment_method and amount:
            # Fetch the donor from the session (make sure the alumni email is set in the session)
            donor = Alumni.objects.filter(alumni_email=request.session.get('alumni_email')).first()

            # Create the donation record in the database
            donation = Donation.objects.create(
                donor=donor,
                amount=amount,
                date=timezone.now().date(),
                payment_method=payment_method,
                notes=notes,
            )

            # Generate the PDF receipt for the donation
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=A4)
            p.setFont("Helvetica", 14)

            p.drawString(100, 800, "🎓 VITGrad - Donation Receipt")
            p.line(100, 795, 500, 795)

            p.drawString(100, 760, f"Donor Name: {donor.alumni_name}")
            p.drawString(100, 740, f"Email: {donor.alumni_email}")
            p.drawString(100, 720, f"Date: {timezone.now().strftime('%d-%m-%Y')}")
            p.drawString(100, 700, f"Payment Method: {payment_method}")
            if upi:
                p.drawString(100, 680, f"UPI ID: {upi}")
            if wallet:
                p.drawString(100, 660, f"Wallet Number: {wallet}")
            p.drawString(100, 640, f"Amount Donated: ₹{amount}")
            p.drawString(100, 620, f"Notes: {notes}")
            p.drawString(100, 580, "✅ Thank you for your generous contribution!")
            p.drawString(100, 560, "This is a system-generated receipt for demonstration purposes.")

            p.showPage()
            p.save()

            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename=VITGrad_Receipt_{donor.alumni_name}.pdf'
            return response

        # If the required fields are missing
        return HttpResponse("<script>alert('Payment failed. Please check required fields.'); window.history.back();</script>")


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
    
@require_POST
def create_post_admin(request):
    content = request.POST.get('content')
    image = request.FILES.get('image')

    print("Content:", content)

    try:
        # Assuming Login is the admin model and admin_email is stored in session
        user = Login.objects.filter(email=request.session.get('admin_email')).first()
        if not user:
            raise Exception("Admin not found")

        print("Admin User:", user)

    except Exception as e:
        print("Error:", str(e))
        return redirect('admindash')  # or display a proper error message

    # Create and save the post with admin (Login model) info
    post = Post.objects.create(
        author_id=str(user._id),  # assuming _id is ObjectIdField
        author_name=user.name,
        author_email=user.email,
        content=content,
        image=image
    )

    print("Post Uploaded Successfully:", post)

    return redirect('admindash')


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

from django.http import JsonResponse
from .models import Event, EventInvitation

def get_event_attendees(request, event_id):
    try:
        event = Event.objects.get(_id=event_id)
        attendees = EventInvitation.objects.filter(event=event, status='accepted').select_related('alumni')

        attendees_list = [{
            'first_name': ai.alumni.first_name,
            'last_name': ai.alumni.last_name,
            'email': ai.alumni.email,
        } for ai in attendees]

        print("------------------------------------")
        print(attendees_list)

        return JsonResponse({
            'event_name': event.event_name,
            'attendees': attendees_list
        })
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)


@require_POST
def create_post(request):
    content = request.POST.get('content')
    image = request.FILES.get('image')

    print(content)

    # Get the current logged-in user's Alumni object (assuming email is in session)
    try:
        alumni = Alumni.objects.filter(alumni_email=request.session.get('alumni_email')).first()
        if not alumni:
            raise Alumni.DoesNotExist
        print(alumni)
    except Alumni.DoesNotExist:
        # Handle gracefully if Alumni is not found
        return redirect('alumnidash')  # or show an error message

    # Create and save the post with author details as strings
    post = Post.objects.create(
        author_id=str(alumni.alumni_id()),  # Assuming alumni_id is a string, you can use alumni_email or username too
        author_name=alumni.alumni_name,
        avatar=alumni.avatar,
        author_email=alumni.alumni_email,
        content=content,
        image=image
    )

    print("Post Uploaded Successfully: ", post)

    return redirect('alumnidash')
