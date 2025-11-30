import os
import logging

import strawberry
from strawberry import auto
import strawberry.django

from .models import ContactMessage
from .gmail_api import send_gmail  


logger = logging.getLogger(__name__)


@strawberry.django.type(ContactMessage)
class ContactMessageType:
    id: auto
    name: auto
    email: auto
    phone: auto
    dept: auto
    message: auto
    created_at: auto


@strawberry.type
class Query:
    hello: str = "API is working!"
    contact_messages: list[ContactMessageType] = strawberry.django.field()


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_contact(
        self,
        name: str,
        email: str,
        phone: str,
        dept: str,
        message: str,
    ) -> ContactMessageType:

        # 1. Save to database
        obj = ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            dept=dept,
            message=message,
        )

        # 2. Build notification email body
        body = (
            "New appointment/contact request received:\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n"
            f"Department: {dept}\n\n"
            "Message:\n"
            f"{message}\n"
        )

        # 3. Send notification email via Gmail API (HTTPS, not SMTP)
        to_email = os.environ.get("NOTIFICATION_EMAIL", "contact@medbary.ca")

        try:
            send_gmail(
                to_email=to_email,
                subject="📩 New Contact/Appointment Request",
                body_text=body,
            )
        except Exception as e:
            # Log error but don't crash the GraphQL mutation
            logger.error("Failed to send Gmail notification", exc_info=e)

        return obj


schema = strawberry.Schema(query=Query, mutation=Mutation)


