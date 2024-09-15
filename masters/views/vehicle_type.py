
from rest_framework import mixins, viewsets
from rest_framework.viewsets import ModelViewSet

from masters.models.vehicle_type import VehicleTypeMasters
from masters.serializers.vehicle_type_master import VehicleTypeSerializer


class VehicleTypeMastersViewSet(ModelViewSet, mixins.CreateModelMixin,
                                     mixins.UpdateModelMixin):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = VehicleTypeSerializer

    def get_queryset(self):
        return VehicleTypeMasters.objects.all()
