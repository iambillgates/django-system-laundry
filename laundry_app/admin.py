from django.contrib import admin
from .models import LaundryOrder

@admin.register(LaundryOrder)
class LaundryOrderAdmin(admin.ModelAdmin):
    list_display = ('e_invoice_number', 'name', 'laundry_type', 'pickup_date', 'pickup_time', 'status', 'created_at')
    list_filter = ('status', 'laundry_type', 'pickup_date')
    search_fields = ('e_invoice_number', 'name', 'whatsapp')
    ordering = ('-created_at',)
