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

class PaymentMethod(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('bank', 'Bank Account'),
        ('upi', 'UPI ID'),
        ('crypto', 'Cryptocurrency'),
        ('paypal', 'PayPal'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Bank Account Fields
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    ifsc_code = models.CharField(max_length=20, null=True, blank=True)

    # UPI Fields
    upi_id = models.CharField(max_length=100, null=True, blank=True)
    account_name = models.CharField(max_length=100, null=True, blank=True)

    # Crypto Fields
    wallet_address = models.CharField(max_length=100, null=True, blank=True)

    # PayPal Fields
    paypal_email = models.EmailField(null=True, blank=True)
    client_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_payment_type_display()} - {self.user.username if self.user else 'System'}"

class Transaction(models.Model):
    PAYMENT_TYPES = (
        ('bank', 'Bank Transfer'),
        ('crypto', 'Cryptocurrency'),
        ('paypal', 'PayPal'),
        ('upi', 'UPI'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    transaction_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    receipt_file = models.FileField(upload_to='receipts/', null=True, blank=True)
    transaction_reference = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.user.username} - {self.amount} {self.currency}"

    class Meta:
        ordering = ['-created_at']

class Withdrawal(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=10)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    account_holder = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.currency} - {self.status}"

    class Meta:
        ordering = ['-created_at']
