from importlib.resources import Package
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from first_operation.models.batch import Batch
from first_operation.models.batch_items import BatchItems
from first_operation.models.batch_log import BatchLog
from first_operation.models.batch_nesting_items import BatchNestingItems
from first_operation.serializer.batch import BatchFullSerializer, BatchItemSerializer, BatchNestingItemSerializer, BatchSerializer


class CreateNewBatchView(APIView):
    # this load only the vehicle details.
    def post(self, request):
        req_data = request.data
        date = req_data.get('date')
        batchNo = req_data.get('batchNo')
        user = self.request.user
        
        try : 
            batch = Batch.objects.get(batch_no=batchNo, status__lt = Batch.Status.Cancelled.value)
            if batch :
               return Response({ "status":False, 
                                 "sameBatchAvailable": True,
                                "message": "Already batch number exisits.Enter new batch no and try again." }, status=status.HTTP_200_OK)
        except Batch.DoesNotExist:
            pass

        batch,_ = Batch.objects.get_or_create(batch_no=batchNo, created_by=user,  updated_by=user, status=0, date=date)  
        serializer = BatchSerializer(batch, partial=True)

        BatchLog.objects.create(log_message="Batch Created Successfully", batch=batch, created_by=user)
        
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
    def get(self, request):
        batchId = request.query_params.get('batchId', None)
        if not batchId:
            batch = Batch.objects.all()
            serializer = BatchSerializer(batch, many=True)
        else :
            try : 
                batch = Batch.objects.get(pk=batchId)
            except Exception as e:
                return Response({'error':True,'error_message': f'{batchId} - Batch not found .'}, status=status.HTTP_404_NOT_FOUND)
            serializer = BatchFullSerializer(batch)

        return Response(serializer.data, status=status.HTTP_200_OK)
    


class UploadNewBatchItemsViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    # this load only the vehicle details.
    def post(self, request):
        serializer = BatchItemSerializer(data=request.data, many=True, partial=True)
        if serializer.is_valid():
            for item in request.data:
                try:
                    batchId = item.get('batch')
                    batch = Batch.objects.get(pk=batchId)
                    batch.updated_by = self.request.user
                    
                    batchItems, created = BatchItems.objects.get_or_create(
                        batch=batch,
                        rm_code=item.get('rmCode'), 
                        item_code = item.get('itemCode'))
                    
                    batchItems.status = 1
                    batchItems.rm_code = item.get('rmCode')
                    batchItems.description = item.get('description')
                    batchItems.thickness = item.get('thickness')   
                    batchItems.item_code = item.get('itemCode')
                    batchItems.qty = item.get('qty')
                    batchItems.sheet_thickness = item.get('sheetThickness')
                    batchItems.material = item.get('material')
                    # batchItems.nesting_count =  item.get('nestingCount')
                    batchItems.created_by = self.request.user
                    batchItems.updated_by = self.request.user
                    batchItems.error = False
                    batchItems.error_message = "Nesting not done"

                    batchItems.save()   
                    batch.status = 1                                        
                    batch.save()
                except Exception as e:
                    return Response(e, status=status.HTTP_400_BAD_REQUEST)
            serializer = BatchFullSerializer(batch)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadNewBatchNestingItemsViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    # this load only the vehicle details.
    def post(self, request):
        serializer = BatchNestingItemSerializer(data=request.data, many=True, partial=True)
        if serializer.is_valid():
            for item in request.data:
                try:
                    batch_item_id= item.get('batchItemId')
                    batchItem = BatchItems.objects.get(pk=batch_item_id)
                    batchItem.updated_by = self.request.user
                    
                    batchNestingItems, created = BatchNestingItems.objects.get_or_create(
                        batch_items=batchItem,
                        nesting_item_code = item.get('nestingItemCode'),
                        nesting_number=item.get('nestingNumber'), 
                       )
                    
                    batchNestingItems.status = 1
                    batchNestingItems.item_qty = item.get('qty')
                    batchNestingItems.sheetThickness = item.get('sheetThickness')
                    batchNestingItems.material = item.get('material')
                    # batchItems.nesting_count =  item.get('nestingCount')
                    batchNestingItems.created_by = self.request.user
                    batchNestingItems.updated_by = self.request.user

                    batchNestingItems.save()   
                    batchItem.status = 1
                    batchItem.save()
                except Exception as e:
                    return Response(e, status=status.HTTP_400_BAD_REQUEST)
            serializer = BatchItemSerializer(batchItem)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
