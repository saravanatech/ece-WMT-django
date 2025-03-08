from rest_framework import serializers

from project.models.part_log import PartLog

class PartLogSerializer(serializers.ModelSerializer):
    part_name = serializers.CharField(source='part.part_number', read_only=True)
    part_description = serializers.CharField(source='part.part_description', read_only=True)
    user_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = PartLog
        fields = ['id', 'part_name', 'part_description', 'project', 'logMessage', 'type',  'created_at', 'user_name']