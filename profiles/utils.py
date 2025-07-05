import requests
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_whatsapp_message(phone_number, message):
    """
    Send a WhatsApp message using the WhatsApp Business API.
    """
    if not all([settings.WHATSAPP_API_KEY, settings.WHATSAPP_PHONE_NUMBER_ID]):
        print("WhatsApp API credentials not configured")
        return False

    url = f"https://graph.facebook.com/v17.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": message}
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Failed to send WhatsApp message: {str(e)}")
        return False

def send_email_notification(to_email, subject, template_name, context):
    """
    Send an email using a template.
    """
    try:
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

def notify_profile_update(user, profile_type):
    """
    Send notifications when a profile is updated.
    """
    if profile_type == 'candidate':
        profile = user.candidate_profile
        if profile.whatsapp_number:
            send_whatsapp_message(
                profile.whatsapp_number,
                f"Your Paydayzz profile has been updated. Log in to view the changes: https://paydayzz.com/profiles/candidate/dashboard/"
            )
        
        send_email_notification(
            user.email,
            "Profile Updated - Paydayzz",
            "profiles/email/profile_updated.html",
            {
                "user": user,
                "profile": profile,
                "profile_type": "candidate"
            }
        )
    
    elif profile_type == 'client':
        profile = user.client_profile
        if profile.whatsapp_number:
            send_whatsapp_message(
                profile.whatsapp_number,
                f"Your Paydayzz company profile has been updated. Log in to view the changes: https://paydayzz.com/profiles/client/dashboard/"
            )
        
        send_email_notification(
            user.email,
            "Company Profile Updated - Paydayzz",
            "profiles/email/profile_updated.html",
            {
                "user": user,
                "profile": profile,
                "profile_type": "client"
            }
        )

def notify_verification_status(user, profile_type, is_verified):
    """
    Send notifications when a profile is verified.
    """
    if profile_type == 'candidate':
        profile = user.candidate_profile
        status = "verified" if is_verified else "pending verification"
        if profile.whatsapp_number:
            send_whatsapp_message(
                profile.whatsapp_number,
                f"Your Paydayzz profile has been {status}. Log in to view your profile status: https://paydayzz.com/profiles/candidate/dashboard/"
            )
        
        send_email_notification(
            user.email,
            f"Profile {status.title()} - Paydayzz",
            "profiles/email/verification_status.html",
            {
                "user": user,
                "profile": profile,
                "is_verified": is_verified
            }
        )
    
    elif profile_type == 'client':
        profile = user.client_profile
        status = "verified" if is_verified else "pending verification"
        if profile.whatsapp_number:
            send_whatsapp_message(
                profile.whatsapp_number,
                f"Your Paydayzz company profile has been {status}. Log in to view your profile status: https://paydayzz.com/profiles/client/dashboard/"
            )
        
        send_email_notification(
            user.email,
            f"Company Profile {status.title()} - Paydayzz",
            "profiles/email/verification_status.html",
            {
                "user": user,
                "profile": profile,
                "is_verified": is_verified
            }
        ) 