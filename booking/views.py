from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin,
    RetrieveModelMixin, UpdateModelMixin
)

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404

from booking.models import Bookings, BookingInfo
from hotel_inventory.models import Rooms
from booking.serializers import(
    BookingRetrieveListSerializer,
    BookingCreateUpdateSerializer,
    BookingInfoRetrieveListSerializer
)
from core.renderers import CustomRenderer
from booking.pagination import BookingPagination




# /============================== bookings API's ==========================/ #

class BookingViewset(
    ListModelMixin, CreateModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin, GenericViewSet
):

    permission_classes = [IsAuthenticated]
    serializer_class = BookingRetrieveListSerializer
    pagination_class = BookingPagination
    renderer_classes = [CustomRenderer]

    action_permissions = {
        "list": [ IsAuthenticated,IsAdminUser ],
        "retrieve": [ IsAuthenticated ],
        "partial_update": [ IsAuthenticated],
        "destroy": [ IsAuthenticated],
        "create": [ IsAuthenticated]
    }

    def get_permissions(self):
        self.permission_classes = self.action_permissions[self.action] 
        return super().get_permissions()
   
   
    

    # The message that will be added in the response for each action in the
    # Viewset
    response_data = {
        "list": {
            "message": "List of booking records",
            "status_code": status.HTTP_200_OK
        },
        "retrieve": {
            "message": "Requested booking record retrieved",
            "status_code": status.HTTP_200_OK
        },
        "partial_update": {
            "message": "Requested booking record updated",
            "status_code": status.HTTP_202_ACCEPTED
        },
        "destroy": {
            "message": "Requested booking record deleted",
            "status_code": status.HTTP_204_NO_CONTENT
        },
        "create": {
            "message": "New booking record created",
            "status_code": status.HTTP_201_CREATED
        }
    }

    def get_object(self):
        booking = get_object_or_404(
            Bookings, 
            uuid = self.kwargs.get("uuid")
        )
        return booking

    def get_queryset(self, *args, **kwargs):
        queryset = Bookings.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return BookingCreateUpdateSerializer
        else:
            return BookingRetrieveListSerializer

   

    def get_renderer_context(self):
        context = super().get_renderer_context()
        if self.action in self.response_data:
            context["message"] = (
                self.response_data.get(self.action).get("message")
            )
            context["status_code"] = (
                self.response_data.get(self.action).get("status_code")
            )
        return context



#  /============================ API to add details of room booking ===================/  #  


class BookingInfoViewset(GenericViewSet):

    # Auth
    permission_classes = [IsAuthenticated]



    def add_details(self, request, *args, **kwargs):
        """
        This API is used to add details of user's room booking 
        """
        #fetching the booking details
        booking_uuid = kwargs.get("booking_uuid")
        booking = Bookings.objects.get(
            uuid = booking_uuid)

        # fetching the room details
        room_uuid = kwargs.get("room_uuid")
        room = Rooms.objects.get(
            uuid = room_uuid,
    )

        #fetching the check_in and check_out
        
        check_in = datetime.strptime(request.data.get("check_in"), "%Y-%m-%d %H:%M:%S")
        check_out = datetime.strptime(request.data.get("check_out"), "%Y-%m-%d %H:%M:%S")

        total_cost = room.cost * booking.no_of_rooms

        details = BookingInfo.objects.create(
            booking = booking,
            room = room,
            check_in = check_in,
            check_out = check_out,
            total_cost = total_cost
        )

        response = {
            "data" : {
                "booking" : details.booking.uuid,
                "room" : details.room.uuid,
                "total_cost" : total_cost,
                "check_in" : check_in,
                "check_out" : check_out
            }
        }

        return Response(
            data = response, 
            status = status.HTTP_202_ACCEPTED
        ) 




    def view_details(self, request, *args, **kwargs):
        """
        This API is used to view details of user's room booking 
        """
        #fetching the details
        bookinginfo = BookingInfo.objects.all()

        serialized_data = BookingInfoRetrieveListSerializer(
            instance=bookinginfo,
            many = True
        ).data

        return Response(
            data={
                "message" : "requested details provided",
                "data" : serialized_data
            },
            status=status.HTTP_200_OK
        )



