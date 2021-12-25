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
    citizen_id = models.CharField(max_length=12, unique=True, blank=True)
    managed_by = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(blank=True, default=date(1, 1, 1))
    place_of_birth = models.CharField(default="unknown", max_length=64)
    place_of_origin = models.CharField(default="unknown", max_length=64)
    permanent_address = models.CharField(blank=True, max_length=64)
    temporary_address = models.CharField(blank=True, max_length=64)
    religious = models.CharField(default="none", max_length=64)
    occupation = models.CharField(default="none", max_length=256)
    education = models.CharField(default="none", max_length=256)
