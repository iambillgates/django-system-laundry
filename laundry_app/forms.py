from django import forms
from .models import LaundryOrder

class LaundryOrderForm(forms.ModelForm):
    class Meta:
        model = LaundryOrder
        fields = [
            'name', 'address', 'whatsapp', 'laundry_type',
            'estimate_kilo', 'payment_method', 'pickup_date', 'pickup_time'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Nama Lengkap'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 2,
                'placeholder': 'Alamat lengkap'
            }),
            'whatsapp': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Nomor WhatsApp'
            }),
            'laundry_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            }),
            'estimate_kilo': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'min': 1,
                'placeholder': 'Estimasi berat (kg)'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Jenis Cucian'
            }),
            'pickup_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Tanggal Ambil'
            }),
            'pickup_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Waktu Ambil'
            }),
        }

class TrackOrderForm(forms.Form):
    e_invoice_number = forms.CharField(
        max_length=20,
        label='E-Faktur Number',
        widget=forms.TextInput(attrs={
            'placeholder': 'Masukkan nomor e-faktur',
            'class': 'flex-grow px-4 py-3 border rounded-lg form-input focus:outline-none focus:border-blue-500'
        })
    )
