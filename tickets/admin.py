from django.contrib import admin
from .models import TicketCounter, TicketTemplate, Ticket
from django.contrib.contenttypes.admin import GenericTabularInline

admin.site.register(TicketCounter)
admin.site.register(TicketTemplate)
admin.site.register(Ticket)
