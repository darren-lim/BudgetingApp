from django.db import models  # databases!
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Transaction(models.Model):
    t_type = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=1000000000, decimal_places=2)
    source = models.CharField(max_length=30)
    notes = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.source

    def get_absolute_url(self):
        # reverse will return the full path as a string so we can redirect to our transaction-detail template page for our newly created transaction
        return reverse('transaction-detail', kwargs={'pk': self.pk})
