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
        fields = ['truckNo', 'truckType', 'status', 'createdBy', 'updatedBy', 'createdAt', 'updatedAt', 'bayInTime', 'bayOutTime', 'id', 'destination']

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
    parts = serializers.SerializerMethodField()


    class Meta:
        model = Vehicle
        fields = ['truckNo', 'truckType', 'status', 'createdBy', 'updatedBy', 'createdAt', 'updatedAt', 
                  'bayInTime', 'bayOutTime', 'id', 'parts','destination']
    
    def get_parts(self, obj):
        # Choose the source based on the destination field value
        parts_source = 'distributon_vehicle_part' if obj.destination == Vehicle.DestinationId.Distribution_Center.value else 'vehicle_part'
        # Get related parts based on the source
        parts = getattr(obj, parts_source, None)
        
        # Serialize the parts using PartSerializer
        return PartSerializer(parts, many=True).data
    
    def to_representation(self, instance):
        # Get the default representation
        representation = super().to_representation(instance)
        
        # Update parts by calling `get_parts`
        representation['parts'] = self.get_parts(instance)
        
        return representation
