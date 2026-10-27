from datetime import datetime

from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    DecimalField,
    DateTimeField,
    DateField
)
from .models import userRegister


class Equipment(Document):

    seller_id = ReferenceField(
        userRegister,
        required=True
    )

    name_equipment = StringField(
        required=True,
        max_length=120
    )

    description = StringField(
        required=True,
        max_length=150
    )

    brand = StringField(
        required=True,
        max_length=120
    )

    model = StringField(
        required=True,
        max_length=120
    )

    price_per_day = DecimalField(
        required=True,
        min_value=0,
        precision=2
    )

    duration = StringField(
        required=True,
        max_length=120
    )

    rating = DecimalField(
        min_value=0,
        max_value=5,
        precision=1,
        default=0
    )

    availability_status = StringField(
        choices=["AVAILABLE", "BOOKED", "UNAVAILABLE"],
        default="AVAILABLE"
    )

    available_from = DateField(required=True)
    available_to = DateField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
