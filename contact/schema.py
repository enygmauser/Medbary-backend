import strawberry
from strawberry import auto
import strawberry.django

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
        return ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            dept=dept,
            message=message
        )


schema = strawberry.Schema(query=Query, mutation=Mutation)
