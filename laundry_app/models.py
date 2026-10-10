from django.db import models
from django.utils.crypto import get_random_string

class LaundryOrder(models.Model):
    LAUNDRY_TYPE_CHOICES = [
        ('daily_kiloan', 'Daily Kiloan'),
        ('cuci_setrika', 'Cuci & Setrika'),
        ('dry_cleaning', 'Dry Cleaning'),
        ('green_dry_cleaning', 'Green Dry Cleaning'),
        ('laundry_sepatu', 'Laundry Sepatu'),
        ('laundry_tas', 'Laundry Tas'),
        ('laundry_karpet', 'Laundry Karpet'),
        ('laundry_gorden', 'Laundry Gorden'),
        ('laundry_kulit', 'Laundry Kulit'),
        ('lainnya', 'Lainnya'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approve', 'Approve'),
        ('proses', 'Proses'),
        ('complete', 'Complete'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]

    e_invoice_number = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=100)
    address = models.TextField()
    whatsapp = models.CharField(max_length=20)
    laundry_type = models.CharField(max_length=30, choices=LAUNDRY_TYPE_CHOICES)
    estimate_kilo = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    biaya = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.e_invoice_number:
            self.e_invoice_number = self.generate_e_invoice_number()
        super().save(*args, **kwargs)

    def generate_e_invoice_number(self):
        from django.utils import timezone
        now = timezone.now()
        # Format: MMDDHHMMSS (Month, Day, Hour, Minute, Second)
        e_invoice = f"{now.month:02d}{now.day:02d}{now.hour:02d}{now.minute:02d}{now.second:02d}"
        
        # Ensure uniqueness by adding a counter if needed
        counter = 1
        original_invoice = e_invoice
        while LaundryOrder.objects.filter(e_invoice_number=e_invoice).exists():
            e_invoice = f"{original_invoice}{counter:02d}"
            counter += 1
        
        return e_invoice

    def __str__(self):
        return f"{self.name} - {self.e_invoice_number}"
