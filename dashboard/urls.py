from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('edit-home/', views.edit_home, name='edit_home'),
    path('edit-feature/', views.edit_feature, name='edit_feature'),
    path('galleries/', views.gallery_list, name='gallery_list'),
    path('edit-gallery/<int:gallery_id>/', views.edit_gallery, name='edit_gallery'),
]