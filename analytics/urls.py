from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.analytics_dashboard, name='dashboard'),
    path('traffic/', views.traffic_overview, name='traffic_overview'),
    path('behavior/', views.user_behavior, name='user_behavior'),
    path('conversions/', views.conversions, name='conversions'),
]