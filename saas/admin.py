from django.contrib import admin
from .models import Plan, Subscription, FeatureLimit

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'max_resorts', 'max_rooms', 'max_users', 'allow_custom_domain', 'trial_days')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active', 'is_trial', 'canceled_at')
    list_filter = ('is_active', 'is_trial')
    search_fields = ('user__email',)

@admin.register(FeatureLimit)
class FeatureLimitAdmin(admin.ModelAdmin):
    list_display = ('plan', 'feature_name', 'limit')
    search_fields = ('feature_name', 'plan__name')
