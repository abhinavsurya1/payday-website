from django.contrib import admin
from .models import WhatsAppNotification

# Register your models here.

@admin.register(WhatsAppNotification)
class WhatsAppNotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_type', 'recipient_name', 'recipient_phone', 'status', 'created_at', 'sent_at')
    list_filter = ('notification_type', 'status', 'created_at')
    search_fields = ('recipient_name', 'recipient_phone')
    readonly_fields = ('created_at', 'sent_at')
    ordering = ('-created_at',)
