from djongo import models
from django.contrib.auth.models import User

# for profile pic
# from PIL import Image


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    initial_amount = models.DecimalField("Initial Balance",
                                         max_digits=10, decimal_places=2, null=True)
    total_amount = models.IntegerField(default=0)
    total_amount_gained = models.IntegerField(default=0)
    total_amount_spent = models.IntegerField(default=0)

    def __str__(self):
        return '{} Profile'.format(self.user.username)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)