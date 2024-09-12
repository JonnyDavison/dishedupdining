from django.urls import path, include
from . import views
from .views import HomePageView, ContactView, contact_success, ServicesPageView, MenuPageView, AboutListView, AboutDetailView, AboutCreateView, AboutUpdateView, AboutDeleteView

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/success/', contact_success, name='contact_success'),
    
    path('about/', AboutListView.as_view(), name='about'),
    path('about/create/', AboutCreateView.as_view(), name='about_create'),
    path('about/<int:pk>/edit/', AboutUpdateView.as_view(), name='about_update'),
    path('about/<int:pk>/delete/', AboutDeleteView.as_view(), name='about_delete'),
    
    path('services/', ServicesPageView.as_view(), name='services'),
    path('menu/', MenuPageView.as_view(), name='menu'),
]