from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import filters

from core.renderers import CustomRenderer
from hotel_inventory.models import Hotels, Rooms
from hotel_inventory.pagination import HotelInventoryPagination
from hotel_inventory.serializers import(
    HotelSerializer,
    RoomCreateUpdateSerializer,
    RoomRetrieveListSerializer
)

# /============================== Hotel API's ==========================/ #


class HotelViewset(
    ListModelMixin, CreateModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin, GenericViewSet
):

    permission_classes = [IsAuthenticated]
    serializer_class = HotelSerializer
    pagination_class = HotelInventoryPagination
    renderer_classes = [CustomRenderer]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


    action_permissions = {
        "list": [ IsAuthenticated ],
        "retrieve": [ IsAuthenticated ],
        "partial_update": [ IsAuthenticated, IsAdminUser],
        "destroy": [ IsAuthenticated, IsAdminUser],
        "create": [ IsAuthenticated, IsAdminUser]
    }

    def get_permissions(self):
        self.permission_classes = self.action_permissions[self.action] 
        return super().get_permissions()
      
    # The message that will be added in the response for each action in the
    # Viewset
    response_data = {
        "list": {
            "message": "List of hotel records",
            "status_code": status.HTTP_200_OK
        },
        "retrieve": {
            "message": "Requested hotel record retrieved",
            "status_code": status.HTTP_200_OK
        },
        "partial_update": {
            "message": "Requested hotel record updated",
            "status_code": status.HTTP_202_ACCEPTED
        },
        "destroy": {
            "message": "Requested hotel record deleted",
            "status_code": status.HTTP_204_NO_CONTENT
        },
        "create": {
            "message": "New hotel record created",
            "status_code": status.HTTP_201_CREATED
        }
    }

    def get_object(self):
        hotels = get_object_or_404(
            Hotels, 
            uuid = self.kwargs.get("uuid")
        )
        return hotels

    def get_queryset(self, *args, **kwargs):
        queryset = Hotels.objects.all()
        return queryset

    def get_serializer_class(self):
        return HotelSerializer   

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



# /============================== rooms API's ==========================/ #

class RoomViewset(
    ListModelMixin, CreateModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin, GenericViewSet
):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomRetrieveListSerializer
    pagination_class = HotelInventoryPagination
    renderer_classes = [CustomRenderer]



    action_permissions = {
        "list": [ IsAuthenticated ],
        "retrieve": [ IsAuthenticated ],
        "partial_update": [ IsAuthenticated, IsAdminUser],
        "destroy": [ IsAuthenticated, IsAdminUser],
        "create": [ IsAuthenticated, IsAdminUser]
    }

    def get_permissions(self):
        self.permission_classes = self.action_permissions[self.action] 
        return super().get_permissions()
   
    

    # The message that will be added in the response for each action in the
    # Viewset
    response_data = {
        "list": {
            "message": "List of room records",
            "status_code": status.HTTP_200_OK
        },
        "retrieve": {
            "message": "Requested room record retrieved",
            "status_code": status.HTTP_200_OK
        },
        "partial_update": {
            "message": "Requested room record updated",
            "status_code": status.HTTP_202_ACCEPTED
        },
        "destroy": {
            "message": "Requested room record deleted",
            "status_code": status.HTTP_204_NO_CONTENT
        },
        "create": {
            "message": "New room record created",
            "status_code": status.HTTP_201_CREATED
        }
    }

    def get_object(self):
        room = get_object_or_404(
            Rooms, 
            uuid = self.kwargs.get("uuid")
        )
        return room

    def get_queryset(self, *args, **kwargs):
        queryset = Rooms.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return RoomCreateUpdateSerializer
        else:
            return RoomRetrieveListSerializer

   

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
