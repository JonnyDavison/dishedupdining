from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Home, Gallery
import os


class HomePageView(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Handle Home data (as we did before)
        home_data = Home.objects.filter(is_active=True).first()
        if home_data:
            if home_data.hero_image and os.path.isfile(home_data.hero_image.path):
                context['hero_image_url'] = home_data.hero_image.url
            else:
                context['hero_image_url'] = None
        else:
            context['hero_image_url'] = None
        context['home'] = home_data

        # Handle Gallery data
        gallery = Gallery.objects.first()  # Assuming you want to display the first gallery
        if gallery:
            gallery_images = []
            for i in range(1, 13):  # Loop through all 12 possible images
                image_field = getattr(gallery, f'gallery_image{i}')
                if image_field and os.path.isfile(image_field.path):
                    gallery_images.append(image_field.url)
            context['gallery_images'] = gallery_images
        else:
            context['gallery_images'] = []

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
