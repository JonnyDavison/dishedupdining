from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Avg
from analytics.models import PageView, DailyAggregate
from index.models import ContactSubmission, Home
import json


def analytics_dashboard(request):
    home = Home.objects.filter(is_active=True).first()
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    
    # Use DailyAggregate for the last 30 days
    daily_data = DailyAggregate.objects.filter(date__gte=thirty_days_ago).order_by('date')
    
    total_views = daily_data.aggregate(Sum('total_views'))['total_views__sum'] or 0
    unique_visitors = daily_data.aggregate(Sum('unique_visitors'))['unique_visitors__sum'] or 0
    new_visitors = daily_data.aggregate(Sum('new_visitors'))['new_visitors__sum'] or 0
    contact_submissions = ContactSubmission.objects.filter(created_at__gte=thirty_days_ago).count()
    avg_time_on_page = daily_data.aggregate(Avg('avg_time_on_page'))['avg_time_on_page__avg']
    
    top_pages = PageView.objects.filter(timestamp__gte=thirty_days_ago) \
        .values('page_url') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:5]
    
    # Prepare data for Chart.js
    dates = [data.date.strftime('%Y-%m-%d') for data in daily_data]
    views = [data.total_views for data in daily_data]
    visitors = [data.unique_visitors for data in daily_data]
    
    chart_data = {
        'dates': dates,
        'views': views,
        'visitors': visitors
    }
    
    context = {
        'home': home,
        'total_views': total_views,
        'unique_visitors': unique_visitors,
        'new_visitors': new_visitors,
        'contact_submissions': contact_submissions,
        'avg_time_on_page': avg_time_on_page,
        'top_pages': top_pages,
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'analytics/analytics_dashboard.html', context)


def traffic_overview(request):
    home = Home.objects.filter(is_active=True).first()
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    
    daily_data = DailyAggregate.objects.filter(date__gte=thirty_days_ago).order_by('date')
    
    total_views = daily_data.aggregate(Sum('total_views'))['total_views__sum'] or 0
    unique_visitors = daily_data.aggregate(Sum('unique_visitors'))['unique_visitors__sum'] or 0
    avg_time_on_page = daily_data.aggregate(Avg('avg_time_on_page'))['avg_time_on_page__avg'] or 0
    
    # Prepare data for Chart.js
    dates = [data.date.strftime('%Y-%m-%d') for data in daily_data]
    views = [data.total_views for data in daily_data]
    visitors = [data.unique_visitors for data in daily_data]
    
    chart_data = {
        'dates': dates,
        'views': views,
        'visitors': visitors
    }
    
    context = {
        'home': home,
        'total_views': total_views,
        'unique_visitors': unique_visitors,
        'avg_time_on_page': avg_time_on_page,
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'analytics/traffic_overview.html', context)

def user_behavior(request):
    home = Home.objects.filter(is_active=True).first()
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    
    daily_data = DailyAggregate.objects.filter(date__gte=thirty_days_ago).order_by('-date')
    
    top_pages = daily_data.values('top_pages').order_by('-total_views')[:10]
    
    # Prepare data for Chart.js
    page_names = [page['top_pages'] for page in top_pages]
    page_views = [page['total_views'] for page in top_pages]
    
    chart_data = {
        'page_names': page_names,
        'page_views': page_views
    }
    
    context = {
        'home': home,
        'top_pages': top_pages,
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'analytics/user_behavior.html', context)

def conversions(request):
    home = Home.objects.filter(is_active=True).first()
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    
    daily_data = DailyAggregate.objects.filter(date__gte=thirty_days_ago).order_by('date')
    
    total_views = daily_data.aggregate(Sum('total_views'))['total_views__sum'] or 0
    total_conversions = daily_data.aggregate(Sum('conversions'))['conversions__sum'] or 0
    
    conversion_rate = (total_conversions / total_views) * 100 if total_views > 0 else 0
    
    # Prepare data for Chart.js
    dates = [data.date.strftime('%Y-%m-%d') for data in daily_data]
    conversions = [data.conversions for data in daily_data]
    
    chart_data = {
        'dates': dates,
        'conversions': conversions
    }
    
    context = {
        'home': home,
        'total_views': total_views,
        'total_conversions': total_conversions,
        'conversion_rate': conversion_rate,
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'analytics/conversions.html', context)