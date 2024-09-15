from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from project.models.parts import Part
from project.models.vehicle import Vehicle
from project.serializer.vehicle import VehicleSerializer, VehicleWithPartSerializer

# API to Create Vehicle
class VehicleCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can create vehicles

    def post(self, request):
        truck_no = request.data.get('truckNo')
        # Check if a vehicle with the same truck_no and active status already exists
        if Vehicle.objects.filter(truck_no=truck_no, status=Vehicle.Status.Active.value).exists():
            return Response({'message': 'A vehicle with this truck number already exists in active state.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            vehcile,_ = Vehicle.objects.get_or_create(truck_no=truck_no)
            vehcile.created_by = self.request.user
            vehcile.save()
            serializer = VehicleSerializer(vehcile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except :
            return Response({'message': f'Something went wrong while creation'}, status=status.HTTP_400_BAD_REQUEST)

# API to Fetch Active Vehicles
class ActiveVehicleListView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can fetch active vehicles

    def get(self, request):
        active_vehicles = Vehicle.objects.filter(status=Vehicle.Status.Active.value)
        serializer = VehicleSerializer(active_vehicles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Recent30VehicleListView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can fetch active vehicles

    def get(self, request):
        active_vehicles = Vehicle.objects.all().order_by('-updated_at')[:30]
        serializer = VehicleSerializer(active_vehicles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VehicleDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can fetch active vehicles

    def get(self, request):
        pk= request.query_params.get('id')
        vehicle = Vehicle.objects.get(pk=pk)
        serializer = VehicleWithPartSerializer(vehicle)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class VehicleUpdateView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can update vehicles

    def put(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            return Response({'error': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VehicleSerializer(vehicle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)  # Set the 'updated_by' field
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class BayTimeView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def get(self, request):
        pk = request.query_params.get('id')
        try:
            vehicle = Vehicle.objects.get(pk=pk)
            parts = Part.objects.filter(vehicle=vehicle) # Assuming 'parts' is the related name in the Part model

            if parts.exists():
                bay_in_time = parts.order_by('updated_at').first().updated_at 
                bay_out_time = parts.order_by('updated_at').last().updated_at  # Last part's updated_at
                vehicle.bay_in_time = bay_in_time
                vehicle.bay_out_time = bay_out_time
                vehicle.save()
                return Response({
                    'bayInTime': bay_in_time,
                    'bayOutTime': bay_out_time
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No parts found for this vehicle.'}, status=status.HTTP_404_NOT_FOUND)
        except Vehicle.DoesNotExist:
            return Response({'message': 'Vehicle not found.'}, status=status.HTTP_404_NOT_FOUND)


class CancelVehicle(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def get(self, request):
        pk = request.query_params.get('id')
        try:
            vehicle = Vehicle.objects.get(pk=pk)
            parts = Part.objects.filter(vehicle=vehicle, vehicle_status__in=(2,4)) # Assuming 'parts' is the related name in the Part model

            if parts.exists():
                return Response({'message': "Some Parts are loaded already, unload all the parts and try cancel again"}, status=status.HTTP_404_NOT_FOUND)
               
            else:
                 vehicle.status= Vehicle.Status.Canceled.value
                 vehicle.save()
                 return Response({ 'message': "Cancelled Successfully" 
                }, status=status.HTTP_200_OK)
        except Vehicle.DoesNotExist:
            return Response({'message': 'Vehicle not found.'}, status=status.HTTP_404_NOT_FOUND)


class ShippedVehicle(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def get(self, request):
        pk = request.query_params.get('id')
        try:
            vehicle = Vehicle.objects.get(pk=pk)
            parts = Part.objects.filter(vehicle=vehicle, vehicle_status__in=(0,1,3)) # Assuming 'parts' is the related name in the Part model

            if parts.exists():
                return Response({'message': "Some Parts are are not loaded, Load all the parts and try Shipped again"}, status=status.HTTP_404_NOT_FOUND)
               
            else:
                 vehicle.status= Vehicle.Status.Shipped.value
                 vehicle.save()

                 return Response({ 'message': "Shipped Successfully" 
                }, status=status.HTTP_200_OK)
        except Vehicle.DoesNotExist:
            return Response({'message': 'Vehicle not found.'}, status=status.HTTP_404_NOT_FOUND)
