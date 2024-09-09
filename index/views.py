from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Home, Gallery, Feature, Review, ContactSubmission
from .forms import ContactForm
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
        active_gallery = Gallery.objects.filter(is_active=True).first()
        if active_gallery:
            gallery_images = []
            for i in range(1, 13):  # Assuming you have 12 image fields
                image_field = getattr(active_gallery, f'gallery_image{i}')
                if image_field and os.path.isfile(image_field.path):
                    gallery_images.append(image_field.url)
            context['gallery_images'] = gallery_images
            context['gallery_name'] = active_gallery.name
            context['gallery_description'] = active_gallery.description
        else:
            context['gallery_images'] = []
            context['gallery_name'] = None
            context['gallery_description'] = None

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
        reviews = Review.objects.all().order_by('-created_at')
        context['reviews'] = reviews

        # Add ContactForm to the context
        context['contact_form'] = ContactForm()

        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            submission = form.save()

            # Send email
            subject = f"New contact form submission: {submission.subject}"
            message = f"Name: {submission.name}\nEmail: {submission.email}\n\nMessage:\n{submission.message}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.CONTACT_EMAIL]

            send_mail(subject, message, from_email, recipient_list)

            # Add a success message to the context
            context = self.get_context_data()
            context['form_submitted'] = True
            return self.render_to_response(context)
        else:
            # If the form is invalid, re-render the page with the form errors
            context = self.get_context_data()
            context['contact_form'] = form
            return self.render_to_response(context)


class ContactView(View):
    template_name = 'index/contact.html'

    def get(self, request):
        form = ContactForm()
        context = {
            'contact_form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            submission = form.save()

            # Send email
            subject = f"New contact form submission: {submission.subject}"
            message = f"Name: {submission.name}\nEmail: {submission.email}\n\nMessage:\n{submission.message}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.CONTACT_EMAIL]

            send_mail(subject, message, from_email, recipient_list)

            # Redirect to a thank you page or the same page with a success message
            return redirect('contact_success')
        
        # If form is not valid, re-render the page with form errors
        context = {
            'contact_form': form
        }
        return render(request, self.template_name, context)

def contact_success(request):
    return render(request, 'index/contact_success.html')


def services(request):
    """
    A view to return the services page
    """
    return render(request, 'index/services.html')


def about(request):
    """
    A view to return the about page
    """
    return render(request, 'index/about.html')


def menu(request):
    """
    A view to return the menu page
    """
    return render(request, 'index/menu.html')
