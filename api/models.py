# api/models.py
# This file is optional for API app, but we can define API logs, tokens, or request tracking here.

from django.db import models
from django.conf import settings
from django.utils.timezone import now

class APILog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    method = models.CharField(max_length=10)
    endpoint = models.CharField(max_length=255)
    request_data = models.TextField(blank=True)
    response_data = models.TextField(blank=True)
    status_code = models.IntegerField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.method} {self.endpoint} [{self.status_code}] at {self.timestamp}"

class APIToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Token for {self.user.email}"
