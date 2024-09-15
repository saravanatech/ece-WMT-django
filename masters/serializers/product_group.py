from rest_framework import serializers
from ..models import (ProductGroupMaster)


class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        """
        """
        model = ProductGroupMaster
        fields = "__all__"
