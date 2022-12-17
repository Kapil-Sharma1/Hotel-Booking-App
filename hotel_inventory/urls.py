from django.urls import path

from hotel_inventory.views import HotelViewset, RoomViewset

app_name = "hotel_inventory"

urlpatterns = [

    # |=============================== Hotels APIs ===========================| #
    path(
        route="hotels/",
        view=HotelViewset.as_view({
            "get": "list",
            "post": "create"
        }),
        name="hotels_list_create"
    ),
    path(
        route="hotels/<slug:uuid>",
        view=HotelViewset.as_view({
            "get": "retrieve",
            "patch": "partial_update",
            "delete": "destroy"
        }),
        name="hotels_retrieve_update_delete"
    ),

       # |=============================== rooms APIs ===========================| #
    path(
        route="rooms/",
        view=RoomViewset.as_view({
            "get": "list",
            "post": "create"
        }),
        name="room_list_create"
    ),
    path(
        route="rooms/<slug:uuid>",
        view=RoomViewset.as_view({
            "get": "retrieve",
            "patch": "partial_update",
            "delete": "destroy"
        }),
        name="room_retrieve_update_delete"
    )
]
