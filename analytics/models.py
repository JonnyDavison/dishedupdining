# analytics/models.py

from django.db import models
from django.contrib.auth.models import User

class PageView(models.Model):
    page_url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    user_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    referrer = models.URLField(null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    time_on_page = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"{self.page_url} viewed at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']


class DailyAggregate(models.Model):
    date = models.DateField(unique=True)
    total_views = models.IntegerField(default=0)
    unique_visitors = models.IntegerField(default=0)
    contact_submissions = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Aggregate for {self.date}"