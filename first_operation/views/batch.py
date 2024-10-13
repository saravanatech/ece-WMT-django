from importlib.resources import Package
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from first_operation.models.batch import Batch
from first_operation.serializer.batch import BatchSerializer


class CreateNewBatchView(APIView):
    # this load only the vehicle details.
    def post(self, request):
        req_data = request.data
        date = req_data.get('date')
        batchNo = req_data.get('batch')
        user = self.request.user
        
        try : 
            batch = Batch.objects.get(batch_no=batchNo, status__lt = Batch.Status.Cancelled.value)
            if batch :
               return Response({ "status":False, 
                                "message": "Already Batch available for selected date." }, status=status.HTTP_200_OK)
        except Batch.DoesNotExist:
            pass

        batch,_ = Batch.objects.get_or_create(batch_no=batchNo, created_by=user, status=0, date=date)  
        serializer = BatchSerializer(batch, partial=True)
        
        return Response( { "status":True,
                           "message":" Batch Created Successfully",
                           "batch": serializer.data } , status=status.HTTP_200_OK)

class CancelBatchView(APIView):
    # this load only the vehicle details.
    def post(self, request):
        req_data = request.data
        batch_id = req_data.get('batch_id')
        
        try : 
            batch = Batch.objects.get(pk=batch_id)
            if batch :
               batch.status = Batch.Status.Cancelled.value
               batch.save()
               serializer = BatchSerializer(batch, partial=True)
               return Response( { "status":True,
                           "message":" Batch Cancelled Successfully",
                           "batch": serializer.data } , status=status.HTTP_200_OK)
        except Batch.DoesNotExist:
            return Response({ "status":False, 
                                "message": "Invalid Batch Id." }, status=status.HTTP_200_OK)
       

class FetchBatchView(APIView):
    serializer_class = BatchSerializer

    def get_queryset(self):
        batch = Batch.objects.filter(status=Batch.Status.Draft.value)
        return batch
    


