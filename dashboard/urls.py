from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('edit-home/', views.edit_home, name='edit_home'),
    path('edit-feature/', views.edit_feature, name='edit_feature'),
    path('galleries/', views.gallery_list, name='gallery_list'),
    path('edit-gallery/<int:gallery_id>/', views.edit_gallery, name='edit_gallery'),
    
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/add/', views.add_review, name='add_review'),
    path('reviews/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('reviews/toggle-approval/<int:review_id>/', views.toggle_review_approval, name='toggle_review_approval'),
    
    path('services-list/', views.service_list, name='service_list'),
    path('services/add/', views.add_service, name='add_service'),
    path('services/edit/<int:service_id>/', views.edit_service, name='edit_service'),
    path('services/delete/<int:service_id>/', views.delete_service, name='delete_service'),
    path('services/toggle-status/<int:service_id>/', views.toggle_service_status, name='toggle_service_status'),
    
    path('about/', views.about_list, name='about_list'),
    path('about/add/', views.add_about, name='add_about'),
    path('about/edit/<int:about_id>/', views.edit_about, name='edit_about'),
    path('about/delete/<int:about_id>/', views.delete_about, name='delete_about'),
    path('about/toggle-status/<int:about_id>/', views.toggle_about_status, name='toggle_about_status'),
    
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/<int:contact_id>/', views.contact_detail, name='contact_detail'),
    path('contacts/<int:contact_id>/toggle-read-status/', views.toggle_contact_read_status, name='toggle_contact_read_status'),
    path('contacts/<int:contact_id>/delete/', views.delete_contact, name='delete_contact'),
     
]