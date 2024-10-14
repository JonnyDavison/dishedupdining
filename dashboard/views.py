from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from index.models import Home, Service, Gallery, Review, ContactSubmission, About, Feature, FeatureItem
from .forms import HomeForm, FeatureForm, GalleryForm, ReviewForm, ServiceForm, AboutForm, FeatureItemFormSet
from django.utils import timezone
from datetime import timedelta
from analytics.models import PageView
from django.db.models import Count, Avg


def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def dashboard_home(request):
    home = Home.objects.filter(is_active=True).first()
    thirty_days_ago = timezone.now() - timedelta(days=30)
    unread_contacts = ContactSubmission.objects.filter(is_read=False).order_by('-created_at')
    read_contacts = ContactSubmission.objects.filter(is_read=True).order_by('-created_at')
    
    total_views = PageView.objects.filter(timestamp__gte=thirty_days_ago).count()
    unique_visitors = PageView.objects.filter(timestamp__gte=thirty_days_ago).values('user_ip').distinct().count()
    new_visitors = PageView.objects.filter(timestamp__gte=thirty_days_ago, user__isnull=True).values('user_ip').distinct().count()
    contact_submissions = ContactSubmission.objects.filter(created_at__gte=thirty_days_ago).count()
    
    top_pages = PageView.objects.filter(timestamp__gte=thirty_days_ago) \
        .values('page_url') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:5]
    
    avg_time_on_page = PageView.objects.filter(timestamp__gte=thirty_days_ago, time_on_page__isnull=False) \
        .aggregate(avg_time=Avg('time_on_page'))['avg_time']
    
    recent_contacts = ContactSubmission.objects.order_by('-created_at')[:5]
    
    context = {
        'home': home,
        'unread_contacts': unread_contacts,
        'read_contacts': read_contacts,
        'total_services': Service.objects.count(),
        'active_galleries': Gallery.objects.filter(is_active=True).count(),
        'total_reviews': Review.objects.count(),
        'recent_contacts': ContactSubmission.objects.order_by('-created_at')[:5],
        'latest_updates': About.objects.order_by('-updated_at')[:5],
        'total_views': total_views,
        'new_visitors': new_visitors,
        'contact_submissions': contact_submissions,
        'top_pages': top_pages,
        'recent_contacts': recent_contacts,
        'avg_time_on_page': avg_time_on_page,
        'unique_visitors': unique_visitors,
    }
    return render(request, 'dashboard/dashboard_home.html', context)

@login_required
@user_passes_test(is_superuser)
def edit_home(request):
    home = Home.objects.filter(is_active=True).first()
    if not home:
        home = Home()
    
    if request.method == 'POST':
        form = HomeForm(request.POST, request.FILES, instance=home)
        if form.is_valid():
            form.save()
            return redirect('dashboard_home')
    else:
        form = HomeForm(instance=home)
    
    context = {
        'form': form,
        'home': home,
    }
    return render(request, 'dashboard/edit_home.html', context)


@login_required
@user_passes_test(is_superuser)
def edit_feature(request):
    home = Home.objects.filter(is_active=True).first()
    feature = Feature.objects.filter(is_active=True).first()
    if not feature:
        feature = Feature()
    
    if request.method == 'POST':
        form = FeatureForm(request.POST, request.FILES, instance=feature)
        formset = FeatureItemFormSet(request.POST, instance=feature)
        if form.is_valid() and formset.is_valid():
            feature = form.save()
            formset.save()
            messages.success(request, 'Feature and Feature Items updated successfully.')
            return redirect('dashboard_home')
    else:
        form = FeatureForm(instance=feature)
        formset = FeatureItemFormSet(instance=feature)
    
    context = {
        'home': home,
        'form': form,
        'formset': formset,
        'feature': feature,
    }
    return render(request, 'dashboard/edit_feature.html', context)


@login_required
@user_passes_test(is_superuser)
def gallery_list(request):
    home = Home.objects.filter(is_active=True).first()
    galleries = Gallery.objects.all()
    
    if request.method == 'POST':
        active_gallery_id = request.POST.get('active_gallery')
        Gallery.objects.all().update(is_active=False)
        Gallery.objects.filter(id=active_gallery_id).update(is_active=True)
        return redirect('gallery_list')
    
    context = {
        'home': home,
        'galleries': galleries,
    }
    return render(request, 'dashboard/gallery_list.html', context)

@login_required
@user_passes_test(is_superuser)
def edit_gallery(request, gallery_id):
    print("Edit gallery view called")  # Debug print
    home = Home.objects.filter(is_active=True).first()
    gallery = get_object_or_404(Gallery, id=gallery_id)
    
    if request.method == 'POST':
        print("POST request received")  # Debug print
        print("FILES:", request.FILES)  # Debug print
        form = GalleryForm(request.POST, request.FILES, instance=gallery)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery updated successfully.')
            return redirect('gallery_list')
        else:
            print("Form errors:", form.errors)  # Debug print
            messages.error(request, 'There was an error updating the gallery. Please check the form.')
    else:
        print("GET request received")  # Debug print
        form = GalleryForm(instance=gallery)
    
    context = {
        'home': home,
        'form': form,
        'gallery': gallery,
    }
    return render(request, 'dashboard/edit_gallery.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def review_list(request):
    home = Home.objects.filter(is_active=True).first()
    reviews = Review.objects.all().order_by('-created_at')
    
    context = {
        'home': home,
        'reviews': reviews,
        }
    return render(request, 'dashboard/review_list.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_review(request):
    home = Home.objects.filter(is_active=True).first()
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review added successfully.')
            return redirect('review_list')
    else:
        form = ReviewForm()
    context = {
        'home': home,
        'form': form,
        }
    
    return render(request, 'dashboard/review_form.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_review(request, review_id):
    home = Home.objects.filter(is_active=True).first()
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully.')
            return redirect('review_list')
    else:
        form = ReviewForm(instance=review)
        
    context = {
        'home': home,
        'form': form,
        'review': review
        }
    return render(request, 'dashboard/review_form.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully.')
        return redirect('review_list')
    return render(request, 'dashboard/delete_review.html', {'review': review})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def toggle_review_approval(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.is_approved = not review.is_approved
    review.save()
    messages.success(request, f'Review {"approved" if review.is_approved else "unapproved"} successfully.')
    return redirect('review_list')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def service_list(request):
    home = Home.objects.filter(is_active=True).first()
    services = Service.objects.all().order_by('name')
    context = {
        'home': home,
        'services': services,
    }
    return render(request, 'dashboard/service_list.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_service(request):
    home = Home.objects.filter(is_active=True).first()
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service added successfully.')
            return redirect('service_list')
    else:
        form = ServiceForm()
    context = {
        'home': home,
        'form': form,
    }
    return render(request, 'dashboard/service_form.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_service(request, service_id):
    home = Home.objects.filter(is_active=True).first()
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully.')
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    context = {
        'home': home,
        'form': form,
        'service': service,
    }
    return render(request, 'dashboard/service_form.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_service(request, service_id):
    home = Home.objects.filter(is_active=True).first()
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted successfully.')
        return redirect('service_list')
    context = {
        'home': home,
        'service': service,
    }
    return render(request, 'dashboard/delete_service.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def toggle_service_status(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.is_active = not service.is_active
    service.save()
    messages.success(request, f'Service {"activated" if service.is_active else "deactivated"} successfully.')
    return redirect('service_list')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def about_list(request):
    home = Home.objects.filter(is_active=True).first()
    abouts = About.objects.all().order_by('-created_at')
    context = {
        'home': home,
        'abouts': abouts,
    }
    return render(request, 'dashboard/about_list.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_about(request):
    home = Home.objects.filter(is_active=True).first()
    if request.method == 'POST':
        form = AboutForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'About page added successfully.')
            return redirect('about_list')
    else:
        form = AboutForm()
    context = {
        'home': home,
        'form': form,
    }
    return render(request, 'dashboard/about_form.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_about(request, about_id):
    home = Home.objects.filter(is_active=True).first()
    about = get_object_or_404(About, id=about_id)
    if request.method == 'POST':
        form = AboutForm(request.POST, request.FILES, instance=about)
        if form.is_valid():
            form.save()
            messages.success(request, 'About page updated successfully.')
            return redirect('about_list')
    else:
        form = AboutForm(instance=about)
    context = {
        'home': home,
        'form': form,
        'about': about,
    }
    return render(request, 'dashboard/about_form.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_about(request, about_id):
    home = Home.objects.filter(is_active=True).first()
    about = get_object_or_404(About, id=about_id)
    if request.method == 'POST':
        about.delete()
        messages.success(request, 'About page deleted successfully.')
        return redirect('about_list')
    context = {
        'home': home,
        'about': about,
    }
    return render(request, 'dashboard/delete_about.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def toggle_about_status(request, about_id):
    about = get_object_or_404(About, id=about_id)
    about.is_active = not about.is_active
    about.save()
    messages.success(request, f'About page {"activated" if about.is_active else "deactivated"} successfully.')
    return redirect('about_list')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def contact_list(request):
    home = Home.objects.filter(is_active=True).first()
    unread_contacts = ContactSubmission.objects.filter(is_read=False).order_by('-created_at')
    read_contacts = ContactSubmission.objects.filter(is_read=True).order_by('-created_at')
    context = {
        'home': home,
        'unread_contacts': unread_contacts,
        'read_contacts': read_contacts,
    }
    return render(request, 'dashboard/contact_list.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def contact_detail(request, contact_id):
    home = Home.objects.filter(is_active=True).first()
    contact = get_object_or_404(ContactSubmission, id=contact_id)
    context = {
        'home': home,
        'contact': contact,
    }
    return render(request, 'dashboard/contact_detail.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def toggle_contact_read_status(request, contact_id):
    contact = get_object_or_404(ContactSubmission, id=contact_id)
    contact.is_read = not contact.is_read
    contact.save()
    status = "read" if contact.is_read else "unread"
    messages.success(request, f'Message marked as {status}.')
    return redirect('contact_list')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_contact(request, contact_id):
    contact = get_object_or_404(ContactSubmission, id=contact_id)
    contact.delete()
    messages.success(request, 'Message deleted successfully.')
    return redirect('contact_list')