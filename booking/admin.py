from django.contrib import admin

from booking.models import Bookings, BookingInfo


admin.site.register(Bookings)
admin.site.register(BookingInfo)