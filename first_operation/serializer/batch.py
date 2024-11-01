
from rest_framework import serializers
from first_operation.models.batch import Batch
from first_operation.models.batch_items import BatchItems
from first_operation.models.batch_log import BatchLog
from first_operation.models.batch_nesting_items import BatchNestingItems


class BatchSerializer(serializers.ModelSerializer):
        
    batchNo = serializers.CharField(source='batch_no')
    createdBy = serializers.CharField(source='created_by')
    updatedBy = serializers.CharField(source='updated_by')
    createdAt = serializers.CharField(source='created_at')
    updatedAt = serializers.CharField(source='updated_at')
    class Meta:
        model = Batch
        fields = ['id','batchNo', 'createdBy', 'updatedBy', 'createdAt' , 'updatedAt', 'status', 'date' ]
        read_only_fields = ['created_at', 'updated_at']


class BatchNestingItemSerializer(serializers.ModelSerializer):
    nestingItemCode = serializers.CharField(source='nesting_item_code')
    nestingNumber = serializers.CharField(source='nesting_number')
    batchItems = serializers.CharField(source='batch_items.id')  # Assuming you want the ID of BatchItems
    itemQty = serializers.IntegerField(source='item_qty')
    createdBy = serializers.CharField(source='created_by')
    updatedBy = serializers.CharField(source='updated_by')
    status = serializers.IntegerField()

    class Meta:
        model = BatchNestingItems
        fields = [
            'id', 'nestingItemCode', 'nestingNumber', 'batchItems', 
            'itemQty', 'createdBy', 'updatedBy', 'status'
        ]




class BatchItemSerializer(serializers.ModelSerializer):
    createdBy = serializers.CharField(source='created_by')
    updatedBy = serializers.CharField(source='updated_by')
    createdAt = serializers.CharField(source='created_at')
    updatedAt = serializers.CharField(source='updated_at')
    rmCode = serializers.CharField(source='rm_code')
    itemCode = serializers.CharField(source='item_code')
    nestingCount = serializers.IntegerField(source='nesting_count')
    sheetThickness = serializers.CharField(source='sheet_thickness')
    errorMessage = serializers.CharField(source='error_message')
    repeatingQty = serializers.CharField(source='repeating_qty')

    nesting_items = BatchNestingItemSerializer(many=True, source='batch_items')
    class Meta:
        model = BatchItems
        fields = [
            'id', 'batch', 'status', 'rmCode', 'itemCode', 'description', 
            'thickness', 'qty', 'sheetThickness', 'material', 
            'nestingCount', 'createdBy', 'updatedBy', 'createdAt', 'updatedAt', 
            'nesting_items','repeatingQty',
            'error', 'errorMessage'
        ]
        read_only_fields = ['createdAt', 'updatedAt']


class BatchLogSerializer(serializers.ModelSerializer):
    class Meta:
        """
        """
        model = BatchLog
        fields = "__all__"

class BatchFullSerializer(serializers.ModelSerializer):
        
    batchNo = serializers.CharField(source='batch_no')
    createdBy = serializers.CharField(source='created_by')
    updatedBy = serializers.CharField(source='updated_by')
    createdAt = serializers.CharField(source='created_at')
    updatedAt = serializers.CharField(source='updated_at')

    items = BatchItemSerializer(many=True, read_only=True, source='batch_items_set')
    activityLogs = BatchLogSerializer(many=True, read_only=True, source='batch_logs')

    class Meta:
        model = Batch
        fields = ['id','batchNo', 'createdBy', 'updatedBy', 'createdAt' , 'updatedAt', 'status', 'date' , 'items', 'activityLogs']
        read_only_fields = ['created_at', 'updated_at']
    