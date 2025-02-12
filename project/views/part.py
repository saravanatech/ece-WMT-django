from importlib.resources import Package
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.utils.timezone import now
from masters.models.vendor import VendorMasters
from project.models.package_index import PackageIndex
from project.models.part_log import PartLog
from project.models.parts import Part
from project.models.rejection_history import VendorRejectionHistory
from project.models.vehicle import Vehicle
from project.serializer.part import PartSerializer, VendorStatsSerializer
import json
from django.db.models import Q

from project.serializer.projectIndex import PackageIndexSerializer
from users.models import UserProfile
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone

from project.utils import fetchPackingSlipForShortQRCodeDetails, fetchPackingSlipQRCodeDetails



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


class VendorStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        user_vendors = user_profile.vendor.all().values_list('name', flat=True)
        today = now().date()

        # Query to fetch the parts related to the vendor
        parts_queryset = Part.objects.filter(qr_code_scanning__in=user_vendors, 
                                             status=Part.Status.MovedToVendor.value)

        # Total number of parts assigned
        total_parts_assigned = parts_queryset.filter(vendor_status__gt=-1).count()

        # Total number of overdue parts
        overdue_parts = parts_queryset.filter(
            mrd__isnull=False
        ).filter(
            mrd__lt=today.strftime("%Y-%m-%d")
        ).count()

        # Total number of parts pending for acceptance
        pending_acceptance_parts = parts_queryset.filter(vendor_status=-3).count()

        # Prepare the response
        stats = {
            "total_parts_assigned": total_parts_assigned,
            "overdue_parts": overdue_parts,
            "pending_acceptance_parts": pending_acceptance_parts,
        }

        serializer = VendorStatsSerializer(stats)
        return Response(serializer.data)


class PartsForAcceptance(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        user_vendors = user_profile.vendor.all().values_list('pk', flat=True)
        today = now().date()

        # Query to fetch the parts related to the vendor
        parts_queryset = Part.objects.filter(vendor__pk__in=user_vendors, 
                                             status=Part.Status.MovedToVendor.value,
                                             vendor_status=Part.VendorStatus.Pending_for_acceptance.value)

        serializer = PartSerializer(parts_queryset, many=True)
        return Response(serializer.data)


class PartsForAcceptanceResponse(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        part_ids = data.get('part_ids', [])
        accepted = data.get('accepted', False)
        reason = data.get('reason','')
        for part_id in part_ids:
            try:
                part = Part.objects.get(id=part_id)
                if accepted:
                    part.vendor_status = Part.VendorStatus.Pending.value
                else:
                    part.vendor_status = Part.VendorStatus.Req_rejected.value
                part.remarks = reason
                part.save()
            except:
                return Response({'error': f'Part with ID {part_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
            try:
                PartLog.objects.create(part=part,project=part.project, logMessage="Vendor Accepted the Part", type='info', created_by=request.user)
            except:
                pass
            
        
        return Response({ "message": "Parts Updated Successfully."}, status=status.HTTP_200_OK)
    

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
                part.vendor_status = Part.VendorStatus.Pending_for_acceptance.value
                part.assigned_time = timezone.now() 
                part.save()
                PartLog.objects.create(part=part,project=part.project, logMessage="Status changed to Moved to Vendor", type='info', created_by=request.user)
                PartLog.objects.create(part=part,project=part.project, logMessage="Assigned to vendor for acceptance ", type='info', created_by=request.user)
                serializer = PartSerializer(part, data=part_data, partial=True)
                if serializer.is_valid(): 
                    updated_parts.append(serializer.data)
            except Part.DoesNotExist:
                return Response({'error': f'Part with ID {part_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
                
        return Response(updated_parts, status=status.HTTP_200_OK)
    

class VendorAcceptedPartsView(APIView):
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
                part.updated_by = self.request.user
                part.vendor_status = Part.VendorStatus.Pending.value
                part.accepted_time = timezone.now()
                part.save()
                PartLog.objects.create(part=part,project=part.project,
                                        logMessage=f'Vendor accepted the part for MRD - {part.mrd} ', 
                                        type='info',
                                        created_by=request.user)
                serializer = PartSerializer(part, data=part_data, partial=True)
                if serializer.is_valid(): 
                    updated_parts.append(serializer.data)
            except Part.DoesNotExist:
                return Response({'error': f'Part with ID {part_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
                
        return Response(updated_parts, status=status.HTTP_200_OK)

class VendorRejectedPartsView(APIView):
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
                part.updated_by = self.request.user
                part.vendor_status = Part.VendorStatus.Req_rejected.value
                part.remarks = part_data['vendorRejectionReason']
                part.save()
                mrd = part.mrd
                PartLog.objects.create(part=part,project=part.project,
                                        logMessage=f'Vendor rejected the part for MRD - {part.mrd}', 
                                        type='info',
                                        created_by=request.user)
                VendorRejectionHistory.objects.create(part=part,
                                                      mrd=mrd,
                                                      vendor=part.vendor,
                                                      assigned_on=part.assigned_time,
                                                      created_by=request.user,
                                                      reason=part_data['vendorRejectionReason'])  
                serializer = PartSerializer(part, data=part_data, partial=True)
                if serializer.is_valid(): 
                    updated_parts.append(serializer.data)
            except Part.DoesNotExist:
                return Response({'error': f'Part with ID {part_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
       
        return Response(updated_parts, status=status.HTTP_200_OK)


class ProjectPagination(PageNumberPagination):
    page_size = 50  # Number of projects per page
    page_size_query_param = 'page_size'
    max_page_size = 50

class FetchRejectedPartsView(APIView):
    pagination_class = ProjectPagination
    def get(self, request):
        
        parts = Part.objects.filter(status=Part.Status.MovedToVendor.value,
                                     vendor_status=Part.VendorStatus.Req_rejected.value).order_by('-updated_at')
        paginator = self.pagination_class()
        paginated_projects = paginator.paginate_queryset(parts, request)
        part_serializer = PartSerializer(paginated_projects, many=True)
        
        return paginator.get_paginated_response(part_serializer.data)
    
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
                part.updated_by = self.request.user
                part.status = Part.Status.Approved.value
                part.vendor_status = Part.VendorStatus.Pending.value
                part.save()
                PartLog.objects.create(part=part,project=part.project,
                                        logMessage=f'Factory acknowledged the rejection ', 
                                        type='info',
                                        created_by=request.user)
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
              if part.vendor_status != Part.VendorStatus.Recieved_In_Factory.value:
                    return Response({'message': "Scan Rejected - " + package_name + " not yet received" }, status=status.HTTP_400_BAD_REQUEST)

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
        

class PartPagenation(PageNumberPagination):
    page_size = 100  # Number of projects per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class GoodsRecieved(APIView):
    pagination_class = PartPagenation
    def post(self, request):
        qr_data = request.data
        
        package_indexes = fetchPackingSlipQRCodeDetails(qr_data)
        if len(package_indexes) == 0:
            return Response({'message': "Scan Rejected -  QR Code is not valid" }, status=status.HTTP_400_BAD_REQUEST)

        for package_index in package_indexes:
            part = package_index.part
            if part.vendor_status > Part.VendorStatus.Packing_Slip_Generated.value or package_index.status > PackageIndex.Status.ReceivedInFactory.value:
                return Response({'message': f'Scan Rejected -  {package_index.packageName} - {part.project.project_no} already received' }, status=status.HTTP_400_BAD_REQUEST)
            
            if part.vendor_status != Part.VendorStatus.Packing_Slip_Generated.value:
                return Response({'message': f'Scan Rejected - {part} must be in Packing Slip Generated status' }, status=status.HTTP_400_BAD_REQUEST)
            
            package_index.status = PackageIndex.Status.ReceivedInFactory.value
            package_index.save()
            
            recievedPackage = PackageIndex.objects.filter(
                                                Q(packageName=part.package_name) &
                                                Q(part=part) &
                                                Q(status__lt= PackageIndex.Status.ReceivedInFactory.value)
                                            )
            if len(recievedPackage) == 0:
                part.vendor_status = Part.VendorStatus.Recieved_In_Factory.value
                part.qc_passed = True
                part.received_time = timezone.now()
                part.save()
            
            
            PartLog.objects.create(
                        part=part,
                        project=part.project,
                        logMessage=f" {package_index.packageName} - {package_index.packAgeIndex} Recevied successfully in package ",
                        type='info',
                        created_by=request.user
                    )
        
        serliazlier = PackageIndexSerializer(package_indexes, many=True)
        return Response(serliazlier.data, status=status.HTTP_200_OK)
    
    def get(self, request):
        # Query to fetch the parts related to the vendor
        parts_queryset = Part.objects.filter(
            status=Part.Status.MovedToVendor.value,
            vendor_status=Part.VendorStatus.Recieved_In_Factory.value
            ).order_by('-updated_at')
        paginator = self.pagination_class()
        paginated_projects = paginator.paginate_queryset(parts_queryset, request)
        
        serializer = PartSerializer(paginated_projects, many=True)
        return paginator.get_paginated_response(serializer.data)




class GoodsQCFailed(APIView):
    pagination_class = PartPagenation
    def post(self, request):
        qr_data = request.data
        package_indexes = fetchPackingSlipQRCodeDetails(qr_data)
        if len(package_indexes) == 0:
            return Response({'message': "Scan Rejected -  QR Code is not valid" }, status=status.HTTP_400_BAD_REQUEST)

        for package_index in package_indexes:
            part = package_index.part
            if part.vendor_status != Part.VendorStatus.Recieved_In_Factory.value:
                return Response({'message': f'Scan Rejected - Goods not yet received' }, status=status.HTTP_400_BAD_REQUEST)
            
            if part.qc_passed == False:
                return Response({'message': f'Scan Rejected -  {package_index.packageName} - {part.project.project_no} already quality rejected' }, status=status.HTTP_400_BAD_REQUEST)
            
            part.qc_passed = False
            part.save()
            PartLog.objects.create(
                    part=part,
                    project=part.project,
                    logMessage=f"Quality Check failed in package - {package_index.packageName}",
                    type='info',
                    created_by=request.user
                )
        
        serliazlier = PackageIndexSerializer(package_indexes, many=True)
        return Response(serliazlier.data, status=status.HTTP_200_OK)
    
    def get(self, request):
        parts_queryset = Part.objects.filter(
            status=Part.Status.MovedToVendor.value,
            vendor_status=Part.VendorStatus.Recieved_In_Factory.value,
            qc_passed=False
            ).order_by('-updated_at')
        paginator = self.pagination_class()
        paginated_projects = paginator.paginate_queryset(parts_queryset, request)
        
        serializer = PartSerializer(paginated_projects, many=True)
        return paginator.get_paginated_response(serializer.data)
    