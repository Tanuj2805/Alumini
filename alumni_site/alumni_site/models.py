from django.db import models

class Login(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.email
    
class Alumni(models.Model):
    alumni_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    alumni_name = models.CharField(max_length=255)
    DOB = models.DateField()
    age = models.IntegerField()
    alumni_email = models.EmailField(unique=True)
    alumni_phone = models.CharField(max_length=20)
    address = models.TextField()
    street_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)

    def __str__(self):
        return self.alumni_name


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=255)
    event_date = models.DateField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.event_name


class Donation(models.Model):
    donation_id = models.AutoField(primary_key=True)
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    purpose = models.TextField()

    def __str__(self):
        return f"Donation {self.donation_id} - {self.alumni.alumni_name}"


class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=255)
    incharge = models.CharField(max_length=255)

    def __str__(self):
        return self.dept_name


class Organization(models.Model):
    alumni = models.OneToOneField(Alumni, on_delete=models.CASCADE)
    org_id = models.AutoField(primary_key=True)
    job_post = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    org_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.org_name


class AlumniEvent(models.Model):
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.alumni.alumni_name} - {self.event.event_name}"
