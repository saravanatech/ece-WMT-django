from rest_framework import serializers

from ..models import (VendorMasters)


class VendorMasterSerializer(serializers.ModelSerializer):
    class Meta:
        """
        """
        model = VendorMasters
        fields = "__all__"
