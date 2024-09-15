from rest_framework import serializers

from project.models.activity_log import ActivityLog

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ['id', 'project_no', 'project', 'description', 'created_at', 'created_by']
        read_only_fields = ['created_at', 'created_by']