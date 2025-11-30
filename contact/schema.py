import strawberry
from strawberry import auto
import strawberry.django

from django.core.mail import send_mail
from django.conf import settings

from .models import ContactMessage


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
    def create_contact(self, name: str, email: str, phone: str, dept: str, message: str) -> ContactMessageType:

        # 1. Save to database
        obj = ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            dept=dept,
            message=message
        )

        # 2. Send notification email
        send_mail(
            subject="📩 New Contact/Appointment Request",
            message=(
                f"New appointment/contact request received:\n\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Department: {dept}\n\n"
                f"Message:\n{message}\n"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["contact@medbary.ca"],
            fail_silently=False,
        )

        return obj


schema = strawberry.Schema(query=Query, mutation=Mutation)
