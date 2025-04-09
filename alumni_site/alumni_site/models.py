from django.db import models
from djongo import models as djongo_models
from django.utils import timezone

class AddressData(models.Model):
    street_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    full_address = models.TextField()

    class Meta:
        abstract = True

class Login(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'login'

class Alumni(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True)
    avatar = models.ImageField(upload_to='static/avatar/', blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    alumni_name = models.CharField(max_length=255)
    DOB = models.DateField()
    age = models.IntegerField()
    alumni_email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  
    alumni_phone = models.CharField(max_length=20)
    address = models.TextField(null=True, blank=True)
    department = models.CharField(max_length=255)
    graduation_year = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.alumni_name

    class Meta:
        db_table = 'alumni'

class Event(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True)
    event_name = models.CharField(max_length=255)
    event_date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    max_participants = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    tags = djongo_models.JSONField(default=list)

    def __str__(self):
        return self.event_name

    class Meta:
        db_table = 'events'

class Donation(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('bank_transfer', 'Bank Transfer'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    _id = djongo_models.ObjectIdField(primary_key=True)
    donor = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    metadata = djongo_models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.donor} - ${self.amount}"

    class Meta:
        db_table = 'donations'

class Department(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True)
    dept_name = models.CharField(max_length=255, unique=True)
    incharge = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.dept_name

    class Meta:
        db_table = 'departments'

class Organization(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True)
    alumni_id = models.CharField(max_length=50)
    job_post = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    org_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    metadata = djongo_models.JSONField(default=dict)

    def __str__(self):
        return self.org_name

    class Meta:
        db_table = 'organizations'

class AlumniEventData(models.Model):
    alumni_id = models.CharField(max_length=50)
    event_id = models.CharField(max_length=50)
    registration_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='registered')
    
    class Meta:
        abstract = True

class AlumniEvent(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True)
    data = djongo_models.EmbeddedField(
        model_container=AlumniEventData,
        default={'alumni_id': '', 'event_id': '', 'status': 'registered'}
    )
    created_at = models.DateTimeField(default=timezone.now)
    metadata = djongo_models.JSONField(default=dict)

    def __str__(self):
        return f"Alumni {self.data.alumni_id} - Event {self.data.event_id}"

    class Meta:
        db_table = 'alumni_events'

class Job(models.Model):
    JOB_TYPES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    )
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('draft', 'Draft'),
    )

    _id = djongo_models.ObjectIdField(primary_key=True)
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=50, choices=JOB_TYPES)
    description = models.TextField()
    requirements = models.TextField()
    application_deadline = models.DateField()
    contact_email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    posted_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    salary_range = djongo_models.JSONField(default=dict)
    skills_required = djongo_models.JSONField(default=list)
    metadata = djongo_models.JSONField(default=dict)

    def __str__(self):
        return f"{self.position} at {self.company}"

    class Meta:
        db_table = 'jobs'
        ordering = ['-posted_date']

# post model
class Post(models.Model):
    author = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='static/posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.alumni_name} - {self.created_at.strftime('%Y-%m-%d')}"
    
    class Meta:
        db_table = 'posts'