from rest_framework import generics

from project.models.package_index import PackageIndex
from project.models.part_log import PartLog
from project.serializer.projectIndex import PackageIndexSerializer

class PackageIndexListByProject(generics.ListAPIView):
    serializer_class = PackageIndexSerializer

    def get_queryset(self):
        part_id = self.kwargs['part_id']
        return PackageIndex.objects.filter(part_id=part_id)
    
