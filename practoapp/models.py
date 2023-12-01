from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    latlong = models.CharField(max_length=50)
    description = models.TextField()
    yoe = models.IntegerField()
    image_url = models.URLField()


from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, default="9999999999")
    city = models.CharField(max_length=100, default="Chennai")
    first_name = models.CharField(max_length=30)  # Adjust the max length as needed
    last_name = models.CharField(max_length=30)  # Adjust the max length as needed
    username = models.CharField(max_length=30, unique=True)  # Adjust the max length as needed
    password = models.CharField(max_length=128)  # Use Django's password hashing, don't store plain text

    # Add related_name to resolve the clash
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

class Appointment(models.Model):
    CANCELLED = 'Cancelled'
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'

    STATUS_CHOICES = [
        (CANCELLED, 'Cancelled'),
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
    ]

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)