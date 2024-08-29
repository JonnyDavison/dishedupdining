from django.views.generic import TemplateView
from .models import Home, Gallery, Feature, Review
import os

class HomePageView(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Home data
        home_data = Home.objects.filter(is_active=True).first()
        if home_data:
            if home_data.hero_image and os.path.isfile(home_data.hero_image.path):
                context['hero_image_url'] = home_data.hero_image.url
            else:
                context['hero_image_url'] = None
            
            if home_data.logo and os.path.isfile(home_data.logo.path):
                context['logo_url'] = home_data.logo.url
            else:
                context['logo_url'] = None
        else:
            context['hero_image_url'] = None
            context['logo_url'] = None
        context['home'] = home_data

        # Gallery data
        gallery = Gallery.objects.first()
        if gallery:
            gallery_images = []
            for i in range(1, 13):  # Assuming you have 12 image fields
                image_field = getattr(gallery, f'gallery_image{i}')
                if image_field and os.path.isfile(image_field.path):
                    gallery_images.append(image_field.url)
            context['gallery_images'] = gallery_images
        else:
            context['gallery_images'] = []

        # Feature data
        feature = Feature.objects.filter(is_active=True).first()
        if feature:
            if feature.feature_image and os.path.isfile(feature.feature_image.path):
                context['feature_image_url'] = feature.feature_image.url
            else:
                context['feature_image_url'] = None
            context['feature'] = feature
            context['feature_items'] = feature.items.all()
        else:
            context['feature'] = None
            context['feature_items'] = []

        # Review data
        reviews = Review.objects.all().order_by('-created_at')[:5]  # Get the 5 most recent reviews
        context['reviews'] = reviews

        return context

def about(request):
    """
    A view to return the about page
    """
    return render(request, 'index/about.html')


def services(request):
    """
    A view to return the services page
    """
    return render(request, 'index/services.html')


def contact(request):
    """
    A view to return the contact page
    """
    return render(request, 'index/contact.html')


def menu(request):
    """
    A view to return the menu page
    """
    return render(request, 'index/menu.html')
