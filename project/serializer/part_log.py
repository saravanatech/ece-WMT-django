from rest_framework import serializers

from project.models.part_log import PartLog

class PartLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartLog
        fields = '__all__'