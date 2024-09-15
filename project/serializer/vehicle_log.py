from rest_framework import serializers

from project.models.vehicle_log import VehicleLog

class PartLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleLog
        fields = '__all__'