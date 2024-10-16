
from rest_framework import mixins, viewsets
from rest_framework.viewsets import ModelViewSet

from first_operation.models.rm_code_master import RMCodeMaster
from first_operation.serializer.rm_code_master import RMCodeMasterSerializer


class RMCodeMastersViewSet(ModelViewSet, mixins.CreateModelMixin,
                                     mixins.UpdateModelMixin):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RMCodeMasterSerializer

    def get_queryset(self):
        return RMCodeMaster.objects.all().order_by("s_no")
