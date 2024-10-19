from django.urls import path
from . import views

urlpatterns = [
    path('set-cookie-consent/', views.set_cookie_consent, name='set_cookie_consent'),
]