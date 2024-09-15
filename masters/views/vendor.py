
from rest_framework import mixins, viewsets
from rest_framework.viewsets import ModelViewSet

from masters.models.vendor import VendorMasters
from masters.serializers.vendor import VendorMasterSerializer

class VendorMastersViewSet(ModelViewSet, mixins.CreateModelMixin,
                                     mixins.UpdateModelMixin):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = VendorMasterSerializer

    def get_queryset(self):
        return VendorMasters.objects.all().order_by("s_no")
