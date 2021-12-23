from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    a1 = "A1"
    a2 = "A2"
    a3 = "A3"
    b1 = "B1"
    b2 = "B2"

    PERMISSION_CHOICES = [
        (a1, "A1"),
        (a2, "A2"),
        (a3, "A3"),
        (b1, "B1"),
        (b2, "B2"),
    ]

    account_id = models.CharField(max_length=8, primary_key=True)
    managed_by = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    permission = models.CharField(max_length=2, choices=PERMISSION_CHOICES)
    name_of_unit = models.CharField(max_length=256)
    classification = models.CharField(max_length=256, blank=True)
    entry_permit = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return self.classification + " " + self.name_of_unit + " (" + self.account_id + ")"
