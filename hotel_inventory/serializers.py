from rest_framework.serializers import(
    ModelSerializer,
    SlugRelatedField
)
from hotel_inventory.models import Hotels, Rooms


class HotelSerializer(ModelSerializer):
    """
    This serializer is responsible for the serialization
    and de-serialization for the hotel model records.
    """

    class Meta:
        model = Hotels
        exclude = ['id']



class RoomCreateUpdateSerializer(ModelSerializer):
    """
    This serializer is responsible for the de-serialization
    for the room model records.
    """

    hotel = SlugRelatedField(
        slug_field="uuid",
        queryset = Hotels.objects.all()
    )

    class Meta:
        model = Rooms
        exclude = ['id']



class RoomRetrieveListSerializer(ModelSerializer):
    """
    This serializer is responsible for serialization 
    for the room model records.
    """
    hotel = HotelSerializer()

    class Meta:
        model = Rooms
        exclude = ['id']


