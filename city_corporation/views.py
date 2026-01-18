from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta, datetime
import json

# Import all models
from citizen.models import Citizen
from holdingtax.models import HoldingTax
from tradelicense.models import TradeLicense
from certification.models import Certification
from tender.models import Tender
from citizencharter.models import CitizenCharter
from complaint.models import Complaint
from complaint.forms import PublicComplaintForm
from tender.models import Tender
from citizencharter.models import CitizenCharter
from contact.models import Contact


def home(request):
    """Home page view"""
    return render(request, 'home.html')


def admin_login(request):
    """Custom admin login view - redirects based on user role"""
    if request.user.is_authenticated:
        return redirect_user_by_role(request)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect_user_by_role(request)
        else:
            return render(request, 'admin/login.html', {'error': 'Invalid username or password'})
    
    return render(request, 'admin/login.html')


def redirect_user_by_role(request):
    """Redirect user based on their group/role."""
    if request.user.is_superuser or request.user.groups.filter(name='SuperAdmin').exists():
        return redirect('dashboard')
    elif request.user.groups.filter(name='citizen').exists():
        return redirect('citizen:citizen_dashboard')
    elif request.user.groups.filter(name='Holding Tax Field Officer').exists():
        return redirect('field_officer:dashboard')
    elif request.user.groups.filter(name='Officer').exists():
        return redirect('officer:dashboard')
    else:
        return redirect('dashboard')  # Default to admin dashboard


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
        'pending': HoldingTax.objects.filter(status='PENDING').count(),
        'paid': HoldingTax.objects.filter(status='PAID').count(),
        'partial': HoldingTax.objects.filter(status='PARTIAL').count(),
        'overdue': HoldingTax.objects.filter(status='OVERDUE').count(),
        'waived': HoldingTax.objects.filter(status='WAIVED').count(),
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


def public_complaint_create(request):
    """Public complaint submission form (no login required)."""
    if request.method == 'POST':
        form = PublicComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            
            # Auto-generate complaint number
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            complaint.complaint_number = f'COMP-{timestamp}'
            
            # Set default status
            complaint.status = 'submitted'
            
            # Try to find citizen by email or phone if provided
            citizen_name = form.cleaned_data.get('citizen_name')
            citizen_email = form.cleaned_data.get('citizen_email')
            citizen_phone = form.cleaned_data.get('citizen_phone')
            
            if citizen_email or citizen_phone:
                citizen = None
                
                if citizen_email:
                    citizen = Citizen.objects.filter(email=citizen_email, is_active=True).first()
                
                if not citizen and citizen_phone:
                    citizen = Citizen.objects.filter(phone_number=citizen_phone, is_active=True).first()
                
                if citizen:
                    complaint.citizen = citizen
            
            complaint.save()
            return redirect('public_complaint_success', complaint_number=complaint.complaint_number)
    else:
        form = PublicComplaintForm()
    
    context = {
        'form': form,
    }
    return render(request, 'complaint/public_form.html', context)


def public_complaint_success(request, complaint_number):
    """Success page after public complaint submission."""
    from django.shortcuts import get_object_or_404
    complaint = get_object_or_404(Complaint, complaint_number=complaint_number)
    context = {
        'complaint': complaint,
    }
    return render(request, 'complaint/public_success.html', context)


def public_tender_list(request):
    """Public tender list (no login required)."""
    tenders = Tender.objects.filter(status='published').order_by('-opening_date')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    
    if search_query:
        tenders = tenders.filter(
            Q(tender_number__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(tenders, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get current time for status checking
    now = timezone.now()
    closing_soon_threshold = now + timedelta(days=7)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'now': now,
        'closing_soon_threshold': closing_soon_threshold,
    }
    return render(request, 'tender/public_list.html', context)


def public_citizencharter_list(request):
    """Public citizen charter list (no login required)."""
    charters = CitizenCharter.objects.filter(is_active=True).order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    service_filter = request.GET.get('service_type', '')
    
    if search_query:
        charters = charters.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if service_filter:
        charters = charters.filter(service_type=service_filter)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(charters, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'service_filter': service_filter,
    }
    return render(request, 'citizencharter/public_list.html', context)
