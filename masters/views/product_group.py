
from rest_framework import mixins, viewsets
from rest_framework.viewsets import ModelViewSet

from masters.models.product_group import ProductGroupMaster
from masters.serializers.product_group import ProductGroupSerializer


class ProductGroupMastersViewSet(ModelViewSet, mixins.CreateModelMixin,
                                     mixins.UpdateModelMixin):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ProductGroupSerializer

    def get_queryset(self):
        return ProductGroupMaster.objects.all().order_by("s_no")
