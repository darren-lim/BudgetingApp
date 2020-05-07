from django.contrib import admin
from .models import Transaction, Total, History

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Total)
admin.site.register(History)
