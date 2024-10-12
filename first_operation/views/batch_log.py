from rest_framework import generics

from first_operation.models.batch import Batch
from first_operation.models.batch_log import BatchLog
from first_operation.serializer.batch import BatchLogSerializer

class BatchLogsByBatchIdViewSet(generics.ListAPIView):
    serializer_class = BatchLogSerializer

    def get_queryset(self):
        batch_id = self.kwargs['batch_id']
        batch = Batch.objects.get(id=batch_id)
        return BatchLog.objects.filter(batch=batch)
    
