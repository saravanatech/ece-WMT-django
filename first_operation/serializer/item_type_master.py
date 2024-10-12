
from rest_framework import serializers
from first_operation.models.item_type_master import ItemTypeMaster

class ItemTypeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        """
        """
        model = ItemTypeMaster
        fields = "__all__"
