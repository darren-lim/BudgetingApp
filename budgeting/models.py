from djongo import models  # databases!
from django.contrib.auth.models import User
from django.urls import reverse


class Total(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    initial_amount = models.DecimalField("Initial Balance",
                                         max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2)
    total_amount_gained = models.DecimalField(
        max_digits=10, decimal_places=2)
    total_amount_spent = models.DecimalField(
        max_digits=10, decimal_places=2)

    # def __str__(self):
    #     return str(self.author)

    # def get_absolute_url(self):
    #     # reverse will return the full path as a string so we can redirect to our budgeting-home template page
    #     return reverse('budgeting-home')

# class Transaction(models.Model):
#     T_TYPE_CHOICES = (('Income', 'INCOME'), ('Expense','EXPENSE'))
#     CATEGORY_CHOICES = (
#         ('Food', 'FOOD'),
#         ('Auto', 'AUTO'),
#         ('Entertainment', 'ENTERTAINMENT'),
#         ('Home', 'HOME'),
#         ('Personal', 'PERSONAL')
#     )
#     t_type = models.CharField("Transaction Type", choices=T_TYPE_CHOICES, max_length=15, null=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     source = models.CharField(
#         "Source (Case Sensitive)", max_length=30)
#     category = models.CharField("Category", choices=CATEGORY_CHOICES, max_length=15, null=True)
#     notes = models.TextField("Additional Information", blank=True, null=True)
#     date_posted = models.DateField("Transaction Date (mm/dd/yyyy)",
#                                    auto_now_add=False, auto_now=False, blank=False, null=True)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     in_history = models.BooleanField(default=False)
#     year = models.IntegerField(null=True)
#     month = models.IntegerField(null=True)

#     class Meta:
#         ordering = ['-date_posted']

#     def __str__(self):
#         return self.source

#     def get_absolute_url(self):
#         # reverse will return the full path as a string so we can redirect to our transaction-detail template page for our newly created transaction
#         return reverse('transaction-detail', kwargs={'pk': self.pk})

#     def add_type(self, typeName):
#         self.t_type = typeName




# class History(models.Model):
#     year = models.IntegerField(null=True)
#     month = models.IntegerField(null=True)
#     monthly_amount_gained = models.DecimalField(
#         max_digits=10, decimal_places=2, null=True)
#     monthly_amount_spent = models.DecimalField(
#         max_digits=10, decimal_places=2, null=True)
#     author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

#     def __str__(self):
#         return "%s/%s" % (self.month, self.year)

#     def get_absolute_url(self):
#         # reverse will return the full path as a string so we can redirect to our budgeting-home template page
#         return reverse('budgeting-home')
