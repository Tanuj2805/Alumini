"""
URL configuration for alumni_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name="index"),
    path('login/', views.login,name="login"),
    path('student_login/', views.student_login,name="student_login"),
    path('admindash/', views.admindash,name="admindash"),
    path('studentdash/', views.studentdash,name="studentdash"),
    path('alumnidash/', views.alumnidash,name="alumnidash"),
    path('logout/', views.logout, name='logout'),
    path('add_alumni/', views.add_alumni, name='add_alumni'),
    path('add_event/', views.add_event, name='add_event'),
    path('add_student/', views.add_student, name='add_student'),
    path('update_alumni_profile/', views.update_alumni_profile, name='update_alumni_profile'),
    path('edit_alumni/', views.edit_alumni, name='edit_alumni'),
    path('delete_alumni/', views.delete_alumni, name='delete_alumni'),
    path('get_alumni_details/', views.get_alumni_details, name='get_alumni_details'),
    
    # Event Management URLs
    path('edit_event/', views.edit_event, name='edit_event'),
    path('delete_event/', views.delete_event, name='delete_event'),
    path('get_event_details/', views.get_event_details, name='get_event_details'),
    
    # Career Management URLs
    path('add_job/', views.add_job, name='add_job'),
    path('delete_job/', views.delete_job, name='delete_job'),
    path('get_job_details/', views.get_job_details, name='get_job_details'),
    
    # Post Management URLs
    path('add_post/', views.add_post, name='add_post'),
    path('edit_post/', views.edit_post, name='edit_post'),
    path('delete_post/', views.delete_post, name='delete_post'),
    path('get_post_details/', views.get_post_details, name='get_post_details'),
    
    # Donation Management URLs
    path('add_donation/', views.add_donation, name='add_donation'),
    path('edit_donation/', views.edit_donation, name='edit_donation'),
    path('delete_donation/', views.delete_donation, name='delete_donation'),
    path('get_donation_details/', views.get_donation_details, name='get_donation_details'),
    path('generate_receipt/', views.generate_receipt, name='generate_receipt'),
    
    # Admin Management URLs
    path('add_admin/', views.add_admin, name='add_admin'),
    path('edit_admin/', views.edit_admin, name='edit_admin'),
    path('delete_admin/', views.delete_admin, name='delete_admin'),
    path('delete_student/', views.delete_student, name='delete_student'),
    path('get_admin_details/', views.get_admin_details, name='get_admin_details'),
    # path('events/', views.events_management, name='events_management'),
    path('send-invitations/', views.send_event_invitations, name='send_event_invitations'),
    path('admindash/<str:event_id>/attendees/', views.get_event_attendees, name='get_event_attendees'),
    path('create_post_admin/', views.create_post_admin, name='create_post_admin'),

    #alumni urls
    path('update_alumni_profile/', views.update_alumni_profile, name='update_alumni_profile'),
    path('create_post/', views.create_post, name='create_post'),
    path('fake_payment/', views.fake_payment, name='fake_payment'),
    path('delete_post/', views.delete_post, name='delete_post'),
    path('respond_to_invitation/', views.respond_to_invitation, name='respond_to_invitation'),

]
