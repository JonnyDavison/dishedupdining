from django.urls import path, include
from . import views
from .views import HomePageView, ContactView, contact_success

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/success/', contact_success, name='contact_success'),
    
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('menu/', views.menu, name='menu'),
]