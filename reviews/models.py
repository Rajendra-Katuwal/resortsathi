from django.db import models
from django.conf import settings
from resorts.models import Resort

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resort = models.ForeignKey(Resort, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # e.g., 1 to 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # for moderation

    def __str__(self):
        return f"Review by {self.user.email} for {self.resort.name}"
