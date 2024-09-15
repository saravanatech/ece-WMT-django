from rest_framework import serializers

from masters.models.vehicle_type import VehicleTypeMasters


from ..models import (VendorMasters)


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        """
        """
        model = VehicleTypeMasters
        fields = "__all__"
