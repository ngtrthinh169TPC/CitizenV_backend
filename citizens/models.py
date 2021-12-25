from datetime import date
from django.db import models

from accounts.models import Account


class Citizen(models.Model):
    male = "Male"
    female = "Female"
    unknown = "unknown"

    GENDER_CHOICES = [
        (male, 'male'),
        (female, 'female'),
        (unknown, 'unknown'),
    ]

    object_id = models.AutoField(primary_key=True)
    citizen_id = models.CharField(
        max_length=12, unique=True, blank=True, null=True)
    managed_by = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=1024)
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(blank=True, default=date(1, 1, 1))
    place_of_birth = models.CharField(max_length=64, blank=True)
    place_of_origin = models.CharField(max_length=64, blank=True)
    permanent_address = models.CharField(max_length=64, blank=True)
    temporary_address = models.CharField(max_length=64, blank=True)
    religious = models.CharField(max_length=64, blank=True)
    occupation = models.CharField(max_length=256, blank=True)
    education = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
