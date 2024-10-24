from django.shortcuts import render
from index.models import Home


def handler404(request, exception):
    """ Error Handler 404 - Page Not Found """
    home = Home.objects.filter(is_active=True).first()
    context = {
        'home': home,
    }
    return render(request, "errors/404.html", context, status=404)
                