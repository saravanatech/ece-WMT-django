
from rest_framework import serializers
from first_operation.models.batch import Batch
from first_operation.models.batch_items import BatchItems
from first_operation.models.batch_log import BatchLog
from first_operation.models.batch_nesting_items import BatchNestingItems

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        """
        """
        model = Batch
        fields = "__all__"


class BatchItemSerializer(serializers.ModelSerializer):
    class Meta:
        """
        """
        model = BatchItems
        fields = "__all__"


class BatchNestingItemSerializer(serializers.ModelSerializer):
    class Meta:
        """
        """
        model = BatchNestingItems
        fields = "__all__"



class BatchLogSerializer(serializers.ModelSerializer):
    class Meta:
        """
        """
        model = BatchLog
        fields = "__all__"
