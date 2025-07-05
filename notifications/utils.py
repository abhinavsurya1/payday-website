from typing import Optional
from .services import WhatsAppNotificationService
from django.conf import settings

def normalize_phone_number(phone: str) -> str:
    """
    Normalize phone number to E.164 format (e.g., 919876543210).
    Removes any spaces, dashes, or other special characters.
    """
    # Remove any non-digit characters
    clean_number = ''.join(filter(str.isdigit, phone))
    
    # If number starts with 0, remove it
    if clean_number.startswith('0'):
        clean_number = clean_number[1:]
    
    # If number doesn't start with country code (91 for India), add it
    if not clean_number.startswith('91'):
        clean_number = f"91{clean_number}"
    
    return clean_number

def send_job_notification(
    candidate_phone: str,
    candidate_name: str,
    job_title: str,
    company: str
) -> Optional[dict]:
    """
    Send WhatsApp notification to a candidate about a job.
    """
    if not settings.WHATSAPP_API_KEY:
        return None

    whatsapp_service = WhatsAppNotificationService()
    normalized_phone = normalize_phone_number(candidate_phone)
    
    return whatsapp_service.send_job_notification_to_candidate(
        phone=normalized_phone,
        candidate_name=candidate_name,
        job_title=job_title,
        company=company
    )

def send_candidate_application_notification(
    client_phone: str,
    client_name: str,
    candidate_name: str,
    job_title: str
) -> Optional[dict]:
    """
    Send WhatsApp notification to a client about a candidate application.
    """
    if not settings.WHATSAPP_API_KEY:
        return None

    whatsapp_service = WhatsAppNotificationService()
    normalized_phone = normalize_phone_number(client_phone)
    
    return whatsapp_service.send_candidate_application_to_client(
        phone=normalized_phone,
        client_name=client_name,
        candidate_name=candidate_name,
        job_title=job_title
    )
