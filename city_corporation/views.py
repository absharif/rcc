from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
import json

# Import all models
from citizen.models import Citizen
from holdingtax.models import HoldingTax
from tradelicense.models import TradeLicense
from certification.models import Certification
from tender.models import Tender
from citizencharter.models import CitizenCharter
from complaint.models import Complaint
from contact.models import Contact


def home(request):
    """Home page view"""
    return render(request, 'home.html')


def admin_login(request):
    """Custom admin login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'admin/login.html', {'error': 'Invalid username or password'})
    
    return render(request, 'admin/login.html')


@require_http_methods(["GET", "POST"])
def logout_view(request):
    """Custom logout view"""
    if request.method == 'POST' and request.user.is_authenticated:
        logout(request)
    # Show logout page for both GET and POST
    return render(request, 'logout.html')


@login_required
def dashboard(request):
    """Custom admin dashboard"""
    # Get counts for all models
    stats = {
        'citizens': Citizen.objects.count(),
        'holding_taxes': HoldingTax.objects.count(),
        'trade_licenses': TradeLicense.objects.count(),
        'certifications': Certification.objects.count(),
        'tenders': Tender.objects.count(),
        'citizen_charters': CitizenCharter.objects.count(),
        'complaints': Complaint.objects.count(),
        'contacts': Contact.objects.count(),
    }
    
    # Payment status counts
    tax_stats = {
        'pending': HoldingTax.objects.filter(payment_status='pending').count(),
        'paid': HoldingTax.objects.filter(payment_status='paid').count(),
        'overdue': HoldingTax.objects.filter(payment_status='overdue').count(),
    }
    
    # License status counts
    license_stats = {
        'pending': TradeLicense.objects.filter(status='pending').count(),
        'approved': TradeLicense.objects.filter(status='approved').count(),
        'expired': TradeLicense.objects.filter(status='expired').count(),
        'rejected': TradeLicense.objects.filter(status='rejected').count(),
    }
    
    # Complaint status counts
    complaint_stats = {
        'submitted': Complaint.objects.filter(status='submitted').count(),
        'in_progress': Complaint.objects.filter(status='in_progress').count(),
        'resolved': Complaint.objects.filter(status='resolved').count(),
        'closed': Complaint.objects.filter(status='closed').count(),
    }
    
    # Certification status counts
    cert_stats = {
        'pending': Certification.objects.filter(status='pending').count(),
        'approved': Certification.objects.filter(status='approved').count(),
        'rejected': Certification.objects.filter(status='rejected').count(),
    }
    
    # Recent activities (last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_citizens = Citizen.objects.filter(created_at__gte=seven_days_ago).count()
    recent_complaints = Complaint.objects.filter(submitted_at__gte=seven_days_ago).count()
    recent_licenses = TradeLicense.objects.filter(created_at__gte=seven_days_ago).count()
    recent_certifications = Certification.objects.filter(created_at__gte=seven_days_ago).count()
    
    context = {
        'stats': stats,
        'tax_stats': tax_stats,
        'license_stats': license_stats,
        'complaint_stats': complaint_stats,
        'cert_stats': cert_stats,
        'recent_citizens': recent_citizens,
        'recent_complaints': recent_complaints,
        'recent_licenses': recent_licenses,
        'recent_certifications': recent_certifications,
        'user': request.user,
    }
    
    return render(request, 'admin/dashboard.html', context)


@login_required
def dashboard_stats_api(request):
    """API endpoint for dashboard statistics charts"""
    # Get data for last 30 days
    days = 30
    dates = []
    citizen_data = []
    complaint_data = []
    license_data = []
    
    for i in range(days):
        date = timezone.now() - timedelta(days=days-i-1)
        dates.append(date.strftime('%Y-%m-%d'))
        
        # Count for each day
        citizen_data.append(
            Citizen.objects.filter(created_at__date=date.date()).count()
        )
        complaint_data.append(
            Complaint.objects.filter(submitted_at__date=date.date()).count()
        )
        license_data.append(
            TradeLicense.objects.filter(created_at__date=date.date()).count()
        )
    
    return JsonResponse({
        'dates': dates,
        'citizens': citizen_data,
        'complaints': complaint_data,
        'licenses': license_data,
    })
