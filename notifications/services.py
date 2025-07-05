import requests
from django.conf import settings
import json
from typing import Dict, Any, Optional
from .models import WhatsAppNotification
from django.utils import timezone

class WhatsAppNotificationService:
    def __init__(self):
        self.api_key = settings.WHATSAPP_API_KEY
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.base_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def send_message(self, to_phone: str, template_name: str, language_code: str = "en", template_components: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send a WhatsApp message using a template.
        """
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        }

        if template_components:
            payload["template"]["components"] = template_components

        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(payload)
            )
            response_data = response.json()
            
            if response.status_code == 200:
                return {"success": True, "data": response_data}
            return {"success": False, "error": response_data.get("error", {}).get("message", "Unknown error")}
            
        except requests.RequestException as e:
            return {"success": False, "error": str(e)}

    def send_job_notification_to_candidate(self, phone: str, candidate_name: str, job_title: str, company: str) -> Dict[str, Any]:
        """
        Send job notification to a candidate.
        """
        # Create notification record
        notification = WhatsAppNotification.objects.create(
            notification_type='job_alert',
            recipient_phone=phone,
            recipient_name=candidate_name,
            content={
                'job_title': job_title,
                'company': company
            }
        )

        template_components = {
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": candidate_name},
                        {"type": "text", "text": job_title},
                        {"type": "text", "text": company}
                    ]
                }
            ]
        }

        result = self.send_message(
            to_phone=phone,
            template_name="job_notification",
            template_components=template_components
        )

        if result.get("success", False):
            notification.mark_as_sent()
        else:
            notification.mark_as_failed(result.get("error", "Unknown error"))

        return result

    def send_candidate_application_to_client(self, phone: str, client_name: str, candidate_name: str, job_title: str) -> Dict[str, Any]:
        """
        Send candidate application notification to a client.
        """
        # Create notification record
        notification = WhatsAppNotification.objects.create(
            notification_type='application',
            recipient_phone=phone,
            recipient_name=client_name,
            content={
                'candidate_name': candidate_name,
                'job_title': job_title
            }
        )

        template_components = {
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": client_name},
                        {"type": "text", "text": candidate_name},
                        {"type": "text", "text": job_title}
                    ]
                }
            ]
        }

        result = self.send_message(
            to_phone=phone,
            template_name="candidate_application",
            template_components=template_components
        )

        if result.get("success", False):
            notification.mark_as_sent()
        else:
            notification.mark_as_failed(result.get("error", "Unknown error"))

        return result
