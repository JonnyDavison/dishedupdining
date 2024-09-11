from django.urls import path, include
from . import views
from .views import HomePageView, ContactView, contact_success, ServicesPageView, AboutPageView, MenuPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/success/', contact_success, name='contact_success'),
    
    path('about/', AboutPageView.as_view(), name='about'),
    path('services/', ServicesPageView.as_view(), name='services'),
    path('menu/', MenuPageView.as_view(), name='menu'),
]