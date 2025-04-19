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
    
    def alumni_id(self):
        return str(self._id)

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
    invited_alumni = models.ManyToManyField(Alumni, through='EventInvitation', related_name='invited_events')

    def event_id(self):
        return str(self._id)

    def __str__(self):
        return self.event_name

class EventInvitation(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined')
    ], default='pending')
    sent_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('event', 'alumni')
    
    def inv_id(self):
        return str(self._id)

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
    donor = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    notes = models.TextField(blank=True)
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
    _id = djongo_models.ObjectIdField(primary_key=True)
    author_id = models.CharField(max_length=255)  # author_id as a string (e.g., username or custom ID)
    avatar = models.ImageField(upload_to='static/avatar/', blank=True, null=True)
    author_name = models.CharField(max_length=255)  # Store the author's name
    author_email = models.EmailField(max_length=255)  # Store the author's email
    content = models.TextField()
    image = models.ImageField(upload_to='static/posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author_name} - {self.created_at.strftime('%Y-%m-%d')}"
    
    def post_id(self):
        return str(self._id)
    
    class Meta:
        db_table = 'posts'

class StudentLogin(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True)
    username = models.PositiveIntegerField(unique=True)  # Numeric only
    password = models.CharField(max_length=128)  # Store hashed password ideally
    name = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} - {self.name}"
    
    class Meta:
        db_table = 'student_login'
