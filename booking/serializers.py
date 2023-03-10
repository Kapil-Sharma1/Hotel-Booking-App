from rest_framework.serializers import(
    ModelSerializer,
    PrimaryKeyRelatedField,
    SlugRelatedField,
    ChoiceField,
    ValidationError
)
from django.contrib.auth.models import User
from booking.models import Bookings, BookingInfo
from hotel_inventory.models import Rooms
from hotel_inventory.serializers import RoomRetrieveListSerializer
from booking.booking_utils import BookingHandler

class BookingCreateUpdateSerializer(ModelSerializer):
    """
    This serializer is responsible for the de-serialization
    for the booking model records.
    """

    user = PrimaryKeyRelatedField(
        queryset = User.objects.all()
    )

    class Meta:
        model = Bookings
        exclude = ['id']


class BookingUpdateSerializer(ModelSerializer):
    """
    This serializer is responsible for the de-serialization
    for the booking model records.
    """

    user = PrimaryKeyRelatedField(
        queryset = User.objects.all()
    )
    booking_status = ChoiceField(
        choices=Bookings.booking_status_choice.choices
    )

    def update(self, instance, validated_data):
        if(
            validated_data['booking_status'] == \
            Bookings.booking_status_choice.CANCELLED.value
        ):
            handler = BookingHandler(instance=instance)
            handler.cancel_booking()
        return super().update(instance, validated_data)

    class Meta:
        model = Bookings
        exclude = ['id']

class BookingRetrieveListSerializer(ModelSerializer):
    """
    This serializer is responsible for the serialization
    for the booking model records.
    """

    class Meta:
        model = Bookings
        exclude = ['id']





class BookingInfoCreateUpdateSerializer(ModelSerializer):
    """
    This serializer is responsible for the de-serialization
    for the booking info model records.
    """


    booking = SlugRelatedField(
        slug_field="uuid",
        queryset = Bookings.objects.all()
    )

    room = SlugRelatedField(
        slug_field="uuid",
        queryset = Rooms.objects.all()
    )

    def validate_date(self):
        if self.check_in > self.check_out:
            raise ValidationError("check_out date must be after check in date")
        

    class Meta:
        model = BookingInfo
        exclude = ['id']



class BookingInfoRetrieveListSerializer(ModelSerializer):
    """
    This serializer is responsible for the serialization
    for the booking info model records.
    """

    room = RoomRetrieveListSerializer()
    booking = BookingRetrieveListSerializer()

    class Meta:
        model = BookingInfo
        exclude = ['id']





