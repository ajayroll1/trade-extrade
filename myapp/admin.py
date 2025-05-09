from django.contrib import admin
from .models import *  # Import all your models

# Register your models
admin.site.register(PaymentMethod)
admin.site.register(Transaction)
admin.site.register(Withdrawal)
# Register any other models you have
