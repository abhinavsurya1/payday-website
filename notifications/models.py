from django.db import models
from django.utils import timezone

# Create your models here.

class WhatsAppNotification(models.Model):
    NOTIFICATION_TYPES = [
        ('job_alert', 'Job Alert to Candidate'),
        ('application', 'Application Alert to Client'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]

    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    recipient_phone = models.CharField(max_length=15)
    recipient_name = models.CharField(max_length=100)
    content = models.JSONField()  # Store template parameters
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['notification_type']),
            models.Index(fields=['status']),
            models.Index(fields=['recipient_phone']),
        ]

    def __str__(self):
        return f"{self.get_notification_type_display()} to {self.recipient_name} ({self.status})"

    def mark_as_sent(self):
        self.status = 'sent'
        self.sent_at = timezone.now()
        self.save()

    def mark_as_failed(self, error_message):
        self.status = 'failed'
        self.error_message = error_message
        self.save()
