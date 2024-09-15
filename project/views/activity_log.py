from rest_framework import generics, permissions

from project.models.activity_log import ActivityLog
from project.serializer.activity_log import ActivityLogSerializer

class ActivityLogCreateView(generics.CreateAPIView):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)