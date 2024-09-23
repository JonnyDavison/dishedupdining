from django.core.management.base import BaseCommand
from django.utils import timezone
from analytics.models import PageView, DailyAggregate
from django.db.models import Count

class Command(BaseCommand):
    help = 'Aggregates daily analytics data'

    def handle(self, *args, **options):
        yesterday = timezone.now().date() - timezone.timedelta(days=1)
        
        daily_views = PageView.objects.filter(timestamp__date=yesterday).count()
        unique_visitors = PageView.objects.filter(timestamp__date=yesterday).values('user_ip').distinct().count()
        
        DailyAggregate.objects.update_or_create(
            date=yesterday,
            defaults={
                'total_views': daily_views,
                'unique_visitors': unique_visitors,
            }
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully aggregated data for {yesterday}'))