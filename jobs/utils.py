from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

def send_shortlisted_notification(application):
    """
    Send a notification email to a candidate when they are shortlisted.
    """
    subject = f'Congratulations! You\'ve been shortlisted for {application.job.title}'
    
    # Render email template
    html_message = render_to_string('emails/shortlisted_notification.html', {
        'application': application,
    })
    
    # Create plain text version
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[application.candidate.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send shortlisted notification email: {str(e)}")
        return False 