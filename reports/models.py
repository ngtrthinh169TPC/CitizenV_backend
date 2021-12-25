from django.db import models
from django.utils import timezone

from accounts.models import Account


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)
    reporter = models.CharField(max_length=2048)
    completed = models.BooleanField(default=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
