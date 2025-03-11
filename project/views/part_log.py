from rest_framework import generics

from project.models.part_log import PartLog
from project.models.parts import Part
from project.models.project import Project
from project.serializer.part_log import PartLogSerializer

class PartLogListByPartID(generics.ListAPIView):
    serializer_class = PartLogSerializer

    def get_queryset(self):
        part_id = self.kwargs['part_id']
        part = Part.objects.get(id=part_id)
        return PartLog.objects.filter(part=part)
    

class PartLogListByProjectID(generics.ListAPIView):
    serializer_class = PartLogSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        project = Project.objects.get(project_no=project_id)
        return PartLog.objects.filter(project=project).order_by("-created_at")