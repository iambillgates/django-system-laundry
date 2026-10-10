from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import LaundryOrder
from .forms import LaundryOrderForm, TrackOrderForm


def home(request):
    if request.method == 'POST':
        form = LaundryOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            # Calculate estimated cost (biaya) based on laundry_type and estimate_kilo
            price_table = {
                'daily_kiloan': (7000, 10000),
                'cuci_setrika': (10000, 15000),
                'dry_cleaning': (25000, 50000),
                'green_dry_cleaning': (30000, 60000),
                'laundry_sepatu': (25000, 50000),
                'laundry_tas': (30000, 100000),
                'laundry_karpet': (15000, 30000),
                'laundry_gorden': (20000, 40000),
                'laundry_kulit': (50000, 150000),
                'lainnya': (0, 0),  # Negotiable
            }

            laundry_type = order.laundry_type
            estimate_kilo = order.estimate_kilo or 0

            # Determine cost calculation method (per kg, per item, per m2, per pair)
            # For simplicity, assume all except 'lainnya' are per kg or per item as given
            # Here, we calculate average price * estimate_kilo for kilo-based types
            if laundry_type in ['daily_kiloan', 'cuci_setrika']:
                avg_price = sum(price_table[laundry_type]) / 2
                order.biaya = avg_price * float(estimate_kilo)
            elif laundry_type in ['dry_cleaning', 'green_dry_cleaning', 'laundry_sepatu', 'laundry_tas', 'laundry_kulit']:
                avg_price = sum(price_table[laundry_type]) / 2
                order.biaya = avg_price * float(estimate_kilo)  # Assuming estimate_kilo as item count
            elif laundry_type in ['laundry_karpet', 'laundry_gorden']:
                avg_price = sum(price_table[laundry_type]) / 2
                order.biaya = avg_price * float(estimate_kilo)  # Assuming estimate_kilo as m2
            else:
                order.biaya = 0  # Negotiable or unknown

            order.save()
            messages.success(request, f'Order placed successfully! Your E-Faktur Number is {order.e_invoice_number}. '
                                      f'Name: {order.name}, Laundry Type: {order.get_laundry_type_display()}, '
                                      f'Estimated Kilo: {order.estimate_kilo}, Payment Method: {order.get_payment_method_display()}')
            return redirect('home')
    else:
        form = LaundryOrderForm()

    track_form = TrackOrderForm()
    context = {
        'form': form,
        'track_form': track_form,
    }
    return render(request, 'laundry_app/home.html', context)

def track_order(request):
    if request.method == 'POST':
        form = TrackOrderForm(request.POST)
        if form.is_valid():
            e_invoice_number = form.cleaned_data['e_invoice_number']
            try:
                order = LaundryOrder.objects.get(e_invoice_number=e_invoice_number)
                return render(request, 'laundry_app/track_result.html', {'order': order})
            except LaundryOrder.DoesNotExist:
                messages.error(request, 'Order with this E-Faktur Number does not exist.')
                return redirect('home')
    return redirect('home')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('admin_login')
    
    return render(request, 'laundry_app/login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required(login_url='admin_login')
def dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Staff only.')
        return redirect('home')
    
    # Get search query
    search_query = request.GET.get('search', '')
    
    # Filter orders based on search query
    if search_query:
        orders = LaundryOrder.objects.filter(
            Q(e_invoice_number__icontains=search_query)
        ).order_by('-created_at')
    else:
        orders = LaundryOrder.objects.all().order_by('-created_at')
    
    return render(request, 'laundry_app/dashboard.html', {
        'orders': orders,
    })

@login_required(login_url='admin_login')
def update_status(request, order_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Staff only.')
        return redirect('home')
    
    if request.method == 'POST':
        order = get_object_or_404(LaundryOrder, id=order_id)
        new_status = request.POST.get('status')
        
        if new_status in dict(LaundryOrder.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order status updated to {order.get_status_display()}')
        else:
            messages.error(request, 'Invalid status value')
    
    return redirect('dashboard')

@login_required(login_url='admin_login')
def delete_order(request, order_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Staff only.')
        return redirect('home')
    
    if request.method == 'POST':
        order = get_object_or_404(LaundryOrder, id=order_id)
        order.delete()
        messages.success(request, 'Order deleted successfully.')
    
    return redirect('dashboard')
