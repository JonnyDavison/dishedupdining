from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import CookieConsent
from django.shortcuts import render
from index.models import Home

@require_POST
def set_cookie_consent(request):
    print("set_cookie_consent view called")
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    consent, created = CookieConsent.objects.get_or_create(session_key=session_key)
    consent.analytics = request.POST.get('analytics') == 'true'
    consent.marketing = request.POST.get('marketing') == 'true'
    consent.preferences = request.POST.get('preferences') == 'true'
    consent.save()

    # Set the session variable for analytics consent
    request.session['cookie_consent_analytics'] = consent.analytics

    return JsonResponse({'status': 'success'})


def policy_view(request, policy_type):
    home = Home.objects.filter(is_active=True).first()
    if policy_type == 'cookie':
        template_name = 'cookie_consent/cookie-policy.html'
        title = 'Cookie Policy'
    elif policy_type == 'privacy':
        template_name = 'cookie_consent/privacy-policy.html'
        title = 'Privacy Policy'
    else:
        # Handle invalid policy type
        return render(request, '404.html')  # Or any other error handling

    context = {
        'home': home,
        'title': title,
        }

    return render(request, template_name, context)