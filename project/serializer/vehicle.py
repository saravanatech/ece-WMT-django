from rest_framework import serializers

from project.models.vehicle import Vehicle
from project.serializer.part import PartSerializer

class VehicleSerializer(serializers.ModelSerializer):

    truckNo = serializers.CharField(source='truck_no')
    truckType = serializers.CharField(source='truck_type')
    bayInTime = serializers.DateTimeField(source='bay_in_time')
    bayOutTime = serializers.DateTimeField(source='bay_out_time')
    createdBy = serializers.CharField(source='created_by.username', allow_blank=True, allow_null=True)
    updatedBy = serializers.CharField(source='updated_by.username', allow_blank=True, allow_null=True)
    updatedBy = serializers.DateTimeField(source='updated_by')
    createdAt = serializers.CharField(source='created_at')
    updatedAt = serializers.CharField(source='updated_at')
    id = serializers.IntegerField(source='pk')

    class Meta:
        model = Vehicle
        fields = ['truckNo', 'truckType', 'status', 'createdBy', 'updatedBy', 'createdAt', 'updatedAt', 'bayInTime', 'bayOutTime', 'id']

class VehicleWithPartSerializer(serializers.ModelSerializer):

    truckNo = serializers.CharField(source='truck_no')
    truckType = serializers.CharField(source='truck_type')
    bayInTime = serializers.DateTimeField(source='bay_in_time')
    bayOutTime = serializers.DateTimeField(source='bay_out_time')
    createdBy = serializers.CharField(source='created_by.username', allow_blank=True, allow_null=True)
    updatedBy = serializers.CharField(source='updated_by.username', allow_blank=True, allow_null=True)
    updatedBy = serializers.DateTimeField(source='updated_by')
    createdAt = serializers.CharField(source='created_at')
    updatedAt = serializers.CharField(source='updated_at')
    id = serializers.IntegerField(source='pk')
    parts = PartSerializer(many=True, read_only=True, source='vehicle_part')


    class Meta:
        model = Vehicle
        fields = ['truckNo', 'truckType', 'status', 'createdBy', 'updatedBy', 'createdAt', 'updatedAt', 'bayInTime', 'bayOutTime', 'id', 'parts']