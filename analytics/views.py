from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Avg
from analytics.models import PageView
from index.models import ContactSubmission, Home


def analytics_dashboard(request):
    home = Home.objects.filter(is_active=True).first()
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    total_views = PageView.objects.filter(timestamp__gte=thirty_days_ago).count()
    unique_visitors = PageView.objects.filter(timestamp__gte=thirty_days_ago).values('user_ip').distinct().count()
    new_visitors = PageView.objects.filter(timestamp__gte=thirty_days_ago, user__isnull=True).values('user_ip').distinct().count()
    contact_submissions = ContactSubmission.objects.filter(created_at__gte=thirty_days_ago).count()
    
    top_pages = PageView.objects.filter(timestamp__gte=thirty_days_ago) \
        .values('page_url') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:5]
    
    avg_time_on_page = PageView.objects.filter(timestamp__gte=thirty_days_ago, time_on_page__isnull=False) \
        .aggregate(avg_time=Avg('time_on_page'))['avg_time']
    
    context = {
        'home': home,
        'total_views': total_views,
        'unique_visitors': unique_visitors,
        'new_visitors': new_visitors,
        'contact_submissions': contact_submissions,
        'top_pages': top_pages,
        'avg_time_on_page': avg_time_on_page,
    }
    return render(request, 'analytics/analytics_dashboard.html', context)


def traffic_overview(request):
    home = Home.objects.filter(is_active=True).first()
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    total_views = PageView.objects.filter(timestamp__gte=thirty_days_ago).count()
    unique_visitors = PageView.objects.filter(timestamp__gte=thirty_days_ago).values('user_ip').distinct().count()
    avg_time_on_page = PageView.objects.filter(timestamp__gte=thirty_days_ago, time_on_page__isnull=False) \
        .aggregate(avg_time=Avg('time_on_page'))['avg_time']
    
    # Daily views for the last 30 days
    daily_views = PageView.objects.filter(timestamp__gte=thirty_days_ago) \
        .values('timestamp__date') \
        .annotate(count=Count('id')) \
        .order_by('timestamp__date')
    
    context = {
        'home': home,
        'total_views': total_views,
        'unique_visitors': unique_visitors,
        'avg_time_on_page': avg_time_on_page,
        'daily_views': daily_views,
    }
    return render(request, 'analytics/traffic_overview.html', context)

def user_behavior(request):
    home = Home.objects.filter(is_active=True).first()
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    top_pages = PageView.objects.filter(timestamp__gte=thirty_days_ago) \
        .values('page_url') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:10]
    
    # Get device types (this is a basic implementation, you might want to use a proper user agent parser)
    device_types = PageView.objects.filter(timestamp__gte=thirty_days_ago) \
        .values('user_agent') \
        .annotate(count=Count('id'))
    
    context = {
        'home': home,
        'top_pages': top_pages,
        'device_types': device_types,
    }
    return render(request, 'analytics/user_behavior.html', context)

def conversions(request):
    home = Home.objects.filter(is_active=True).first()
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    total_views = PageView.objects.filter(timestamp__gte=thirty_days_ago).count()
    contact_submissions = ContactSubmission.objects.filter(created_at__gte=thirty_days_ago).count()
    
    conversion_rate = (contact_submissions / total_views) * 100 if total_views > 0 else 0
    
    # Daily conversions for the last 30 days
    daily_conversions = ContactSubmission.objects.filter(created_at__gte=thirty_days_ago) \
        .values('created_at__date') \
        .annotate(count=Count('id')) \
        .order_by('created_at__date')
    
    context = {
        'home': home,
        'total_views': total_views,
        'contact_submissions': contact_submissions,
        'conversion_rate': conversion_rate,
        'daily_conversions': daily_conversions,
    }
    return render(request, 'analytics/conversions.html', context)
