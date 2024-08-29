from django.urls import path, include
from . import views
from .views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('menu/', views.menu, name='menu'),
]