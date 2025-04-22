from django.db import models
from django.contrib.auth.models import User

class Trade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=20)
    type = models.CharField(max_length=4)  # BUY or SELL
    quantity = models.DecimalField(max_digits=10, decimal_places=8)
    entry_price = models.DecimalField(max_digits=20, decimal_places=8)
    total_amount = models.DecimalField(max_digits=20, decimal_places=8)
    status = models.CharField(max_length=20)  # open, closed, failed
    created_at = models.DateTimeField(auto_now_add=True)
    stop_loss = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    take_profit = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    profit = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    commission = models.DecimalField(max_digits=20, decimal_places=8, default=0)

    class Meta:
        ordering = ['-created_at']
