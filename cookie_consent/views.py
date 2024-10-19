from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import CookieConsent

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