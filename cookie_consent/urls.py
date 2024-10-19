from django.urls import path
from . import views
from .views import policy_view

urlpatterns = [
    path('set-cookie-consent/', views.set_cookie_consent, name='set_cookie_consent'),
    path('<str:policy_type>/', policy_view, name='policy_view'),
]