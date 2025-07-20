from django.db import models
from django.conf import settings
from django.utils import timezone
from accounts.models import User


class Plan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    max_resorts = models.PositiveIntegerField(default=1)
    max_rooms = models.PositiveIntegerField(default=50)
    max_users = models.PositiveIntegerField(default=10)
    allow_custom_domain = models.BooleanField(default=False)
    trial_days = models.PositiveIntegerField(default=14)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_trial = models.BooleanField(default=True)
    canceled_at = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        if not self.is_active:
            return False
        if self.end_date and timezone.now() > self.end_date:
            return False
        return True

    def __str__(self):
        return f"{self.user.email} - {self.plan.name if self.plan else 'No Plan'}"

class FeatureLimit(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='limits')
    feature_name = models.CharField(max_length=100)
    limit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.plan.name} - {self.feature_name}: {self.limit}"
    

# class Tenant(models.Model):
#     name = models.CharField(max_length=255)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_tenants')
#     users = models.ManyToManyField(User, through='TenantUser')
#     subscription = models.OneToOneField('Subscription', on_delete=models.CASCADE)
#     domain = models.CharField(max_length=255, unique=True, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


# class TenantUser(models.Model):
#     ROLE_CHOICES = (
#         ('tenant_admin', 'Tenant Admin'),
#         ('manager', 'Manager'),
#         ('staff', 'Staff'),
#         ('viewer', 'Viewer'),
#     )
#     tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)
#     joined_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('tenant', 'user')

#     def __str__(self):
#         return f"{self.user.email} - {self.tenant.name} ({self.role})"
