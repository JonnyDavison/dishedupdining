from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from index.models import Home, Service, Gallery, Review, ContactSubmission, About, Feature, FeatureItem
from .forms import HomeForm, FeatureForm, GalleryForm

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def dashboard_home(request):
    home = Home.objects.filter(is_active=True).first()
    context = {
        'home': home,
        'total_services': Service.objects.count(),
        'active_galleries': Gallery.objects.filter(is_active=True).count(),
        'total_reviews': Review.objects.count(),
        'recent_contacts': ContactSubmission.objects.order_by('-created_at')[:5],
        'latest_updates': About.objects.order_by('-updated_at')[:5],
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
        if form.is_valid():
            form.save()
            return redirect('dashboard_home')
    else:
        form = FeatureForm(instance=feature)
    
    context = {
        'home': home,
        'form': form,
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
    home = Home.objects.filter(is_active=True).first()
    gallery = get_object_or_404(Gallery, id=gallery_id)
    
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES, instance=gallery)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery updated successfully.')
            return redirect('gallery_list')
        else:
            messages.error(request, 'There was an error updating the gallery. Please check the form.')
    else:
        form = GalleryForm(instance=gallery)  # Initialize form for GET requests
    
    context = {
        'home': home,
        'form': form,
        'gallery': gallery,
    }
    return render(request, 'dashboard/edit_gallery.html', context)