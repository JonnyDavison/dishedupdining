from django.db import models

class CookieConsent(models.Model):
    session_key = models.CharField(max_length=40, unique=True)
    analytics = models.BooleanField(default=False)
    marketing = models.BooleanField(default=False)
    preferences = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)