from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField()
    payee = models.CharField(max_length=100, blank=True, null=True)
    memo = models.CharField(max_length=100, blank=True, null=True)
    delta = models.DecimalField(max_digits=11, decimal_places=2)
