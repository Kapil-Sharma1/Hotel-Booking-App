from django.db import models

from core.behaviours import UUIDMixin


class Hotels(UUIDMixin):
    """
    This model represents hotels
    """
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    total_rooms = models.IntegerField()


    class Meta:
        db_table = "hotels"
        verbose_name = "hotel"
        verbose_name_plural = "hotel"

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name






class Rooms(UUIDMixin):
    """
    This model represent a room.
    A hotel can have many rooms.
    """
    hotel = models.ForeignKey(
        to= Hotels,
        on_delete=models.PROTECT,
        related_name="rooms",
        related_query_name="room"
    )

    room_no = models.IntegerField()

    class room_type_choice(models.TextChoices):
        SINGLE = ("SINGLE","Single")
        DOUBLE = ("DOUBLE","Double")
        TRIPLE = ("TRIPLE","Triple")
        QUAD = ("QUAD","Quad")

    room_type = models.CharField(
        max_length=50,
        choices=room_type_choice.choices
    )

    cost = models.IntegerField()



    class Meta:
        db_table = "rooms"
        verbose_name = "room"
        verbose_name_plural = "rooms"

    def __repr__(self) -> str:
        return f"{self.hotel} : {self.room_type}"

    def __str__(self) -> str:
        return f"{self.hotel} : {self.room_type}"
