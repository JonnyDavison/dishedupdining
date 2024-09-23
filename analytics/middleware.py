from .models import PageView
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone

class PageViewMiddleware(MiddlewareMixin):
    def process_request(self, request):
        excluded_paths = ['/admin/', '/analytics/', '/dashboard/', '/profiles/', '/media/', '/favicon.ico']
        
        if not any(request.path.startswith(path) for path in excluded_paths):
            user = request.user if request.user.is_authenticated else None
            user_ip = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT')
            referrer = request.META.get('HTTP_REFERER')
            session_key = request.session.session_key

            PageView.objects.create(
                page_url=request.path,
                user=user,
                user_ip=user_ip,
                user_agent=user_agent,
                referrer=referrer,
                session_key=session_key
            )

            # Store the start time of the page view in the session
            request.session['page_view_start'] = timezone.now().isoformat()

        return None

    def process_response(self, request, response):
        if 'page_view_start' in request.session:
            start_time = timezone.datetime.fromisoformat(request.session['page_view_start'])
            end_time = timezone.now()
            time_on_page = end_time - start_time

            try:
                # Get the most recent PageView for this session
                page_view = PageView.objects.filter(session_key=request.session.session_key).latest('timestamp')
                # Update its time_on_page
                page_view.time_on_page = time_on_page
                page_view.save()
            except PageView.DoesNotExist:
                # Handle the case where no PageView exists for this session
                pass

            del request.session['page_view_start']

        return response