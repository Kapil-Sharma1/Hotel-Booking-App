from django.urls import path

from booking.views import BookingViewset, BookingInfoViewset

app_name = "booking"

urlpatterns = [

    # |=============================== booking APIs ===========================| #
    path(
        route="",
        view=BookingViewset.as_view({
            "get": "list",
            "post": "create"
        }),
        name="booking_list_create"
    ),
    path(
        route="<slug:uuid>",
        view=BookingViewset.as_view({
            "get": "retrieve",
            "patch": "partial_update",
            "delete": "destroy"
        }),
        name="booking_retrieve_update_delete"
    ),

     # |=============================== booking info APIs ===========================| #

        path(
        route='bookinginfo/<slug:booking_uuid>/room/<slug:room_uuid>/',
        view=BookingInfoViewset.as_view({
            'post' : 'add_details',
             
        })
    ),

    path(
        route="bookinginfo/details/",
        view=BookingInfoViewset.as_view({
            "get" : "view_details"
        }),
        
    )
]
