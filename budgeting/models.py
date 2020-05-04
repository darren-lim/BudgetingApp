from django.db import models  # databases!
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from .fields import ListTextWidget
from django import forms


class Transaction(models.Model):
    t_type = models.CharField(max_length=15, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField("Source (e.g. Part-time job, My Bank Account)", max_length=30)
    notes = models.TextField("Additional Information", blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.source

    def get_absolute_url(self):
        # reverse will return the full path as a string so we can redirect to our transaction-detail template page for our newly created transaction
        return reverse('transaction-detail', kwargs={'pk': self.pk})

    def add_type(self, typeName):
        self.t_type = typeName


# class Deposit(Transaction):