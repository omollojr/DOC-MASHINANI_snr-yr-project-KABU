from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='media/', blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(null=True)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    id_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)  # Increased max_length
    email = models.EmailField()
    county = models.CharField(max_length=100)
    subcounty = models.CharField(max_length=100)
    emergency_name = models.CharField(max_length=100)
    emergency_relationship = models.CharField(max_length=100)
    emergency_phone_number = models.CharField(max_length=20)  # Increased max_length
    medical_hitory = models.CharField(max_length=100)

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

class Services(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Access_id = models.CharField(max_length=100)
    service_name = models.CharField(max_length=100)
    email = models.EmailField()
    date_time = models.DateField()
    next_visit_date = models.DateField()
    notes = models.TextField()
    refer_to_hospital = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')])

    def __str__(self):
        return self.service_name
    
    