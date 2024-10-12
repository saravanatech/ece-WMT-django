
from rest_framework import mixins, viewsets
from rest_framework.viewsets import ModelViewSet

from first_operation.models.item_type_master import ItemTypeMaster
from first_operation.serializer.item_type_master import ItemTypeMasterSerializer


class ItemTypeMasterViewSet(ModelViewSet, mixins.CreateModelMixin,
                                     mixins.UpdateModelMixin):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ItemTypeMasterSerializer

    def get_queryset(self):
        return ItemTypeMaster.objects.all().order_by("s_no")
