from importlib.resources import Package
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication



from masters.models.vendor import VendorMasters
from project.models.package_index import PackageIndex
from project.models.part_log import PartLog
from project.models.parts import Part
from project.models.vehicle import Vehicle
from project.serializer.part import PartSerializer
import json
from django.db.models import Q


class BulkPartUpdateView(APIView):
    def post(self, request):
        parts_data = request.data
        
        if not isinstance(parts_data, list):
            return Response({'error': 'Input data must be a list of parts.'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_parts = []
        for part_data in parts_data:
            part_id = part_data.get('id')
            try :
                part_data['partPackageMapping'] = json.dumps(part_data['partPackageMapping'])
            except :
                part_data['partPackageMapping'] = ''
            if not part_id:
                return Response({'error': 'Each part must have an ID.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                part = Part.objects.get(id=part_id)
            except Part.DoesNotExist:
                return Response({'error': f'Part with ID {part_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
                
            part.updated_by = self.request.user
            # old_values = {field.name: getattr(part, field.name) for field in part._meta.get_fields() if hasattr(part, field.name)}  # Capture old values
            serializer = PartSerializer(part, data=part_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                updated_parts.append(serializer.data)
                part = Part.objects.get(id=part_id)
                if part.vendor is None or  part.vendor.name != part_data['vendor']:
                    vendor = VendorMasters.objects.get(name=part_data['vendor'])
                    part.vendor = vendor
                    part.save()
                log_message = part_data['changeLog']
                PartLog.objects.create(
                    part=part,
                    project=part.project,
                    logMessage=log_message,
                    type='info',
                    created_by=request.user
                )
                # PartLog.objects.create(part=part,project=part.project, logMessage="Field Updated", type='info', created_by=request.user)

                # part = Part.objects.get(id=part_id)
                # part.vendor = VendorMasters.objects.filter(name=part_data['vendor'])[0]

                # part.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(updated_parts, status=status.HTTP_200_OK)



class PartECNtUpdateView(APIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        parts_data = request.data
        
        if not isinstance(parts_data, list):
            return Response({'error': 'Input data must be a list of parts.'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_parts = []
        for part_data in parts_data:
            part_id = part_data.get('id')
            try :
                part_data['partPackageMapping'] = json.dumps(part_data['partPackageMapping'])
            except :
                part_data['partPackageMapping'] = ''
            if not part_id:
                return Response({'error': 'Each part must have an ID.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                part = Part.objects.get(id=part_id)
                part.updated_by = self.request.user
                serializer = PartSerializer(part, data=part_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    updated_parts.append(serializer.data)
                    part.is_ecn = True
                    part.vendor_status = Part.VendorStatus.Pending.value
                    part.part_package_mapping = {}
                    part.save()
                    packageIndexs = PackageIndex.objects.filter(ProjectNo=part.project.project_no, 
                                                                packageName=part.package_name)
                    for packIndex in packageIndexs:
                        packIndex.revision = packIndex.revision + 1
                        packIndex.save()
                    PartLog.objects.create(part=part,project=part.project, logMessage="ECN fields Updated", type='info', created_by=request.user)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Part.DoesNotExist:
                return Response({'error': f'Part with ID {part_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': f'Part with ID {part_id} not found.'}, status=status.HTTP_404_NOT_FOUND)

            
        
        return Response(updated_parts, status=status.HTTP_200_OK)



class PartVehicleLoadingUpdateView(APIView):
    # this load only the vehicle details.
    def post(self, request):
        parts_data = request.data
        
        if not isinstance(parts_data, list):
            return Response({'error': 'Input data must be a list of parts.'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_parts = []
        for part_data in parts_data:
            part_id = part_data.get('id')
            try :
                part_data['partPackageMapping'] = json.dumps(part_data['partPackageMapping'])
            except :
                part_data['partPackageMapping'] = ''
            if not part_id:
                return Response({'error': 'Each part must have an ID.'}, status=status.HTTP_400_BAD_REQUEST)
            vehicle = Vehicle.objects.filter(truck_no=part_data['truckNo'], status=0).first()
            try:
                part = Part.objects.get(id=part_id)
                part.updated_by = self.request.user
                if vehicle.destination == Vehicle.DestinationId.Distribution_Center.value :
                    part.distribution_vehicle = vehicle
                else : 
                    part.vehicle = vehicle
                serializer = PartSerializer(part, data=part_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    updated_parts.append(serializer.data)
                    if vehicle.destination == Vehicle.DestinationId.Distribution_Center.value :
                        part.distribution_vehicle_status = Part.DistributionVehicleStatus.TrukDataLoaded.value
                    else :
                        part.vehicle_status = Part.VechileStatus.TrukDataLoaded.value
                    PartLog.objects.create(part=part,project=part.project, logMessage="Vechile Details Updated {vheicle}", type='info', created_by=request.user)
                    part.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Part.DoesNotExist:
                return Response({'error': f'Part with ID {part_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response(e, status=status.HTTP_404_NOT_FOUND)

            
        
        return Response(updated_parts, status=status.HTTP_200_OK)



class MovePartToVendorView(APIView):
    def post(self, request):
        parts_data = request.data
        
        if not isinstance(parts_data, list):
            return Response({'error': 'Input data must be a list of parts.'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_parts = []
        for part_data in parts_data:
            part_id = part_data.get('id')
            try :
                part_data['partPackageMapping'] = json.dumps(part_data['partPackageMapping'])
            except :
                part_data['partPackageMapping'] = ''
            if not part_id:
                return Response({'error': 'Each part must have an ID.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                try:
                    vendor=VendorMasters.objects.filter(name=part_data['vendor']).first()
                except :
                    return Response({'error': f'Selected Vendor not found.'}, status=status.HTTP_404_NOT_FOUND)
                part_data['vendor'] = vendor.pk
                part = Part.objects.get(id=part_id)
                part.status = Part.Status.MovedToVendor.value
                part.updated_by = self.request.user
                part.save()
                PartLog.objects.create(part=part,project=part.project, logMessage="Status changed to Moved to Vendor", type='info', created_by=request.user)
                serializer = PartSerializer(part, data=part_data, partial=True)
                if serializer.is_valid(): 
                    updated_parts.append(serializer.data)
            except Part.DoesNotExist:
                return Response({'error': f'Part with ID {part_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
                
        return Response(updated_parts, status=status.HTTP_200_OK)


class MovePartToDoneView(APIView):
    def post(self, request):
        parts_data = request.data
        
        if not isinstance(parts_data, list):
            return Response({'error': 'Input data must be a list of parts.'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_parts = []
        for part_data in parts_data:
            part_id = part_data.get('id')
            try :
                part_data['partPackageMapping'] = json.dumps(part_data['partPackageMapping'])
            except :
                part_data['partPackageMapping'] = ''
            if not part_id:
                return Response({'error': 'Each part must have an ID.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                part = Part.objects.get(id=part_id)
                part.status = Part.Status.FullyCompleted.value
                part.updated_by = self.request.user
                part.save()
                PartLog.objects.create(part=part,project=part.project, logMessage="Status Changed to Fully Completed", type='info', created_by=request.user)
                serializer = PartSerializer(part, data=part_data, partial=True)
                if serializer.is_valid(): 
                    updated_parts.append(serializer.data)
            except Part.DoesNotExist:
                return Response({'error': f'Part with ID {part_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
                
        return Response(updated_parts, status=status.HTTP_200_OK)
    
class MovePartToApprovedrView(APIView):
    def post(self, request):
        parts_data = request.data
        
        if not isinstance(parts_data, list):
            return Response({'error': 'Input data must be a list of parts.'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_parts = []
        for part_data in parts_data:
            part_id = part_data.get('id')
            try :
                part_data['partPackageMapping'] = json.dumps(part_data['partPackageMapping'])
            except :
                part_data['partPackageMapping'] = ''
            if not part_id:
                return Response({'error': 'Each part must have an ID.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                part = Part.objects.get(id=part_id)
                part.status = Part.Status.Approved.value
                part.updated_by = self.request.user
                PartLog.objects.create(part=part,project=part.project, logMessage="Status changed to Approved", type='info', created_by=request.user)
                part.save()
                serializer = PartSerializer(part, data=part_data, partial=True)
                if serializer.is_valid(): 
                    updated_parts.append(serializer.data)
            except Part.DoesNotExist:
                return Response({'error': f'Part with ID {part_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
                
        return Response(updated_parts, status=status.HTTP_200_OK)

class PartQRGeneratedView(APIView):
    def post(self, request):
        parts_data = request.data
        
        if not isinstance(parts_data, list):
            return Response({'error': 'Input data must be a list of parts.'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_parts = []
        for part_data in parts_data:
            part_id = part_data.get('id')
            try :
                part_data['partPackageMapping'] = json.dumps(part_data['partPackageMapping'])
            except :
                part_data['partPackageMapping'] = ''
            if not part_id:
                return Response({'error': 'Each part must have an ID.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                part = Part.objects.get(id=part_id)
                part.vendor_status = Part.VendorStatus.QR_Generated.value
                part.updated_by = self.request.user
                part.save()
                PartLog.objects.create(part=part,project=part.project, logMessage="QR generated", type='info', created_by=request.user)
                serializer = PartSerializer(part, data=part_data, partial=True)
                if serializer.is_valid(): 
                    updated_parts.append(serializer.data)
            except Part.DoesNotExist:
                return Response({'error': f'Part with ID {part_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
                
        return Response(updated_parts, status=status.HTTP_200_OK)


class PartPackageAllocationView(APIView):
    def post(self, request):
        parts_data = request.data
        
        if not isinstance(parts_data, list):
            return Response({'error': 'Input data must be a list of parts.'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_parts = []
        for part_data in parts_data:
            part_id = part_data.get('id')
            if not part_id:
                return Response({'error': 'Each part must have an ID.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                part = Part.objects.get(id=part_id)
                part.vendor_status = Part.VendorStatus.package_allocation_done.value
                partPackageMapping = part_data['partPackageMapping']
                unique_values = set(partPackageMapping.values())
                for value in unique_values:
                    keys = ','.join(str(k) for k, v in partPackageMapping.items() if v == value)
                    package,_ = PackageIndex.objects.get_or_create(part=part, packageName=part_data['packageName'], packAgeIndex=value)
                    package.partsSelectedIndex = keys
                    package.ProjectNo =  part_data['projectNo']
                    package.status = PackageIndex.Status.AllocationDone.value
                    package.save()
                
                part_data['partPackageMapping'] = json.dumps(partPackageMapping)
                part.part_package_mapping = json.dumps(partPackageMapping)
                part.updated_by = self.request.user
                PartLog.objects.create(part=part,project=part.project, logMessage="Package Allocation Completed", type='info', created_by=request.user)
                part.save()

                serializer = PartSerializer(part, data=part_data, partial=True)
                if serializer.is_valid(): 
                    updated_parts.append(serializer.data)
            except Part.DoesNotExist:
                return Response({'error': f'Part with ID {part_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
                
        return Response(updated_parts, status=status.HTTP_200_OK)
    


class PartPackingSlipGeneratedView(APIView):
    def post(self, request):
        parts_data = request.data
        
        if not isinstance(parts_data, list):
            return Response({'error': 'Input data must be a list of parts.'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_parts = []
        for part_data in parts_data:
            part_id = part_data.get('id')
            
            try :
                part = Part.objects.get(id=part_id)
                # partPackageMapping is { partIndex : packageIndex} -> ex: {"1": 1, "2": 1, "3": 2, "4": 2}
                partPackageMapping = part_data['partPackageMapping']
                unique_values = set(partPackageMapping.values())
                for value in unique_values:
                    package= PackageIndex.objects.get(part=part, packageName=part_data['packageName'], packAgeIndex=value)
                    package.status = PackageIndex.Status.PackingSlipGenerated.value
                    package.save()
                try:
                    part_data['partPackageMapping'] = json.dumps(part_data['partPackageMapping'])
                except Exception as e:
                    part_data['partPackageMapping'] = ''
            
            except Exception as e:
                return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)


            if not part_id:
                return Response({'error': 'Each part must have an ID.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                part.vendor_status = Part.VendorStatus.Packing_Slip_Generated.value
                part.updated_by = self.request.user
                part.save()
                PartLog.objects.create(part=part,project=part.project, logMessage="Packing Slip Generated and Printed", type='info', created_by=request.user)

                serializer = PartSerializer(part, data=part_data, partial=True)
                if serializer.is_valid(): 
                    updated_parts.append(serializer.data)
            except Part.DoesNotExist:
                return Response({'error': f'Part with ID {part_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
                
        return Response(updated_parts, status=status.HTTP_200_OK)


class ScannedWhileLoadingView(APIView):
    def post(self, request):
        parts_data = request.data
        package_name = parts_data.get('package_name')
        parts = parts_data.get('parts')
        package_index = parts_data.get('package_index')
        vehicle_id = parts_data.get('vehicle_id')
        revision = parts_data.get('revision',1)

        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
        except:
             return Response({'message': 'Vehicle is not active'}, status=status.HTTP_400_BAD_REQUEST)
        updated_parts = []
        for part_id in parts:
            try :
              part = Part.objects.get(id=part_id)
              print(part)
              if part.qr_type == 'Type-2':
                packageIndexs = PackageIndex.objects.filter(part=part,packageName=package_name, packAgeIndex=package_index)
                if len(packageIndexs)== 0:
                    continue
                else :
                    packageIndex = packageIndexs[0]
                    if packageIndex.revision != revision:
                        return Response({'message': "Scan Rejected -  Scan the latest " + package_name + " packing slip" }, status=status.HTTP_400_BAD_REQUEST)
                    if packageIndex.status == PackageIndex.Status.Loaded.value:
                        PartLog.objects.create(part=part,project=part.project, logMessage="Package scanned second time which was already loaded", type='error', created_by=request.user)
                        return Response({'message': package_name + " Already Loaded" }, status=status.HTTP_400_BAD_REQUEST)
                    packageIndex.status = PackageIndex.Status.Loaded.value
                    packageIndex.save()
              else:
                try:
                    packageIndex = PackageIndex.objects.get(part=part,packageName=package_name,packAgeIndex=package_index)
                    if packageIndex.revision != revision:
                            return Response({'message': "Scan Rejected -  Scan the latest " + package_name + " packing slip" }, status=status.HTTP_400_BAD_REQUEST)
                        
                    if packageIndex.status == PackageIndex.Status.Loaded.value:
                        PartLog.objects.create(part=part,project=part.project, logMessage="Package scanned second time which was already loaded", type='error', created_by=request.user)
                        return Response({'message': package_name + " Already Loaded" }, status=status.HTTP_400_BAD_REQUEST)
                    packageIndex.status = PackageIndex.Status.Loaded.value
                    packageIndex.save()
                except:
                    continue
            except :
                return Response({'message': 'Each part must have an ID.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                notLoadedPackageIndex = PackageIndex.objects.filter(
                                                Q(packageName=package_name) &
                                                Q(part=part) &
                                                Q(status__lt=10)
                                            )

                if len(notLoadedPackageIndex) != 0:
                    if vehicle.destination == Vehicle.DestinationId.Distribution_Center.value:
                        part.distribution_vehicle_status = Part.DistributionVehicleStatus.PartiallyLoaded.value
                    else :
                        part.vehicle_status = Part.VechileStatus.PartiallyLoaded.value
                        part.status = Part.Status.PartiallyLoaded.value
                    PartLog.objects.create(part=part,project=part.project, logMessage=f"Package Loaded partially into vechile - {vehicle}", type='info', created_by=request.user)       
                else:
                    if vehicle.destination == Vehicle.DestinationId.Distribution_Center.value:
                        part.distribution_vehicle_status = Part.DistributionVehicleStatus.LoadedInTruck.value
                        part.status = Part.Status.DCDelivered.value
                    else:
                        part.vehicle_status = Part.VechileStatus.LoadedInTruck.value
                        part.status = Part.Status.Delivered.value
                    PartLog.objects.create(part=part,project=part.project, logMessage=f"Package Loaded fully into vechile - {vehicle}", type='info', created_by=request.user)

                part.updated_by = self.request.user
                part.save()
                updated_parts.append(part)

            except Part.DoesNotExist:
                return Response({'error': f'Part with ID {part_id} not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PartSerializer(updated_parts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
                
class ScannedWhileUnLoading(APIView):
    def post(self, request):
        parts_data = request.data
        package_name = parts_data.get('package_name')
        parts = parts_data.get('parts')
        package_index = parts_data.get('package_index')
        revision = parts_data.get('revision',1)
        vehicle_id = parts_data.get('vehicle_id')
        
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
        except:
             return Response({'message': 'Vehicle is not active'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_parts = []
        for part_id in parts:
            try :
              part = Part.objects.get(id=part_id)
              if part.qr_type == 'Type-2':
                packageIndexs = PackageIndex.objects.filter(part=part,packageName=package_name, packAgeIndex=package_index)
                if len(packageIndexs)== 0:
                    continue
                else :
                    packageIndex = packageIndexs[0] 
                    if packageIndex.revision != revision:
                        return Response({'message': "Scan Rejected -  Scan the latest " + package_name + " packing slip" }, status=status.HTTP_400_BAD_REQUEST)
                    
                    packageIndex.status = PackageIndex.Status.UnLoaded.value
                    packageIndex.save()
              else:
                try:
                    packageIndex = PackageIndex.objects.get(part=part,packageName=package_name,packAgeIndex=package_index)
                    if packageIndex.revision != revision:
                            return Response({'message': "Scan Rejected -  Scan the latest " + package_name + " packing slip" }, status=status.HTTP_400_BAD_REQUEST)
                    packageIndex.status = PackageIndex.Status.UnLoaded.value
                    packageIndex.save()
                except: 
                    continue
            except :
                return Response({'error': 'Each part must have an ID.'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                notLoadedPackageIndex = PackageIndex.objects.filter(
                                                Q(packageName=package_name) &
                                                Q(part=part) &
                                                Q(status__gt=9)
                                            )

                if len(notLoadedPackageIndex) != 0:
                    if vehicle.destination == Vehicle.DestinationId.Distribution_Center.value:
                        part.distribution_vehicle_status = Part.DistributionVehicleStatus.PartiallyLoaded.value
                    else:
                        part.vehicle_status = Part.VechileStatus.PartiallyLoaded.value
                    part.status = Part.Status.PartiallyLoaded.value
                    PartLog.objects.create(part=part,project=part.project, logMessage=f"Package unloaded partially from vechile - {vehicle}", type='info', created_by=request.user)
                else:
                    if vehicle.destination == Vehicle.DestinationId.Distribution_Center.value:
                        part.distribution_vehicle_status = Part.DistributionVehicleStatus.UnLoaded.value
                    else:    
                        part.vehicle_status = Part.VechileStatus.UnLoaded.value
                    part.status = Part.Status.MovedToVendor.value
                    PartLog.objects.create(part=part,project=part.project, logMessage=f"Package unloaded fully from vechile - {vehicle}", type='info', created_by=request.user)
                part.updated_by = self.request.user
                part.save()
                updated_parts.append(part)

            except Part.DoesNotExist:
                return Response({'error': f'Part with ID {part_id} not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PartSerializer(updated_parts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
                
