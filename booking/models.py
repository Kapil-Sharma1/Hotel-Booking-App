from django.db import models

from django.contrib.auth.models import User
from core.behaviours import UUIDMixin

from model_utils.models import TimeStampedModel
from hotel_inventory.models import Rooms


class Bookings(UUIDMixin, TimeStampedModel):
    """
    This model represents bookings by the users.
    """

    user = models.ForeignKey(
        to=User,
        on_delete=models.PROTECT,
        related_name="bookings",
        related_query_name="booking"
    )

    no_of_rooms = models.IntegerField(default=1)

    class booking_status_choice(models.TextChoices):
        BOOKED = ("BOOKED","Booked")
        COMPLETED = ("COMPLETED","Completed")
        CANCELLED = ("CANCELLED","Cancelled")
        

    booking_status = models.CharField(
        max_length=50,
        choices=booking_status_choice.choices,
        default=booking_status_choice.BOOKED.value
    )


    class Meta:
        db_table = "bookings"
        verbose_name = "booking"
        verbose_name_plural = "bookings"

    def __repr__(self) -> str:
        return f"{self.user} : {self.no_of_rooms} : {self.booking_status}"

    def __str__(self) -> str:
        return f"{self.user} : {self.no_of_rooms} : {self.booking_status}"



class BookingInfo(UUIDMixin):
    """
    This model represents the details of bookings.
    """

    booking = models.ForeignKey(
        to=Bookings,
        on_delete=models.PROTECT,
        related_name="bookingsinfo",
        related_query_name="bookinginfo"
    )

    room = models.ForeignKey(
        to=Rooms,
        on_delete=models.PROTECT,
        related_name="booking_rooms",
        related_query_name="booking_room"
    )

    total_cost = models.IntegerField(null=True, blank=True)

    check_in = models.DateTimeField()
    check_out = models.DateTimeField()


    class Meta:
        db_table = "bookinginfo"
        verbose_name = "bookinginfo"
        verbose_name_plural = "bookinginfo"

    def __repr__(self) -> str:
        return f"{self.booking} : {self.room}"

    def __str__(self) -> str:
        return f"{self.booking} : {self.room}"
