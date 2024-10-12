from django.urls import path

from first_operation.views.batch_log import BatchLogsByBatchIdViewSet
from first_operation.views.item_type_master import ItemTypeMasterViewSet
from first_operation.views.rm_code_master import RMCodeMastersViewSet


urlpatterns = [
    path('item-type-master/', ItemTypeMasterViewSet.as_view(), name='item-type-master'),
    path('rm-code-master/', RMCodeMastersViewSet.as_view(), name='rm-code-masters'),
    path('batch_log', BatchLogsByBatchIdViewSet.as_view(), name='batch-log')
]