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
    closing_price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

class WishlistItem(models.Model):
    CATEGORY_CHOICES = [
        ('CRYPTO', 'Cryptocurrency'),
        ('STOCKS', 'Stocks'),
        ('INDICES', 'Indices'),
        ('COMMODITIES', 'Commodities'),
        ('FOREX', 'Forex'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=20)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    added_at = models.DateTimeField(auto_now_add=True)
    last_price = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    price_change = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        unique_together = ['user', 'symbol']
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} - {self.symbol}"
