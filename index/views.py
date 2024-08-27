from django.shortcuts import render

# Create your views here.
def index(request):
    """
    A view to return the index page
    """
    return render(request, 'index/index.html')


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
