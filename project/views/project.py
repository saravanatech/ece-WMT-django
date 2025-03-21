from collections import defaultdict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from project.models import Project
from project.models.parts import Part
from project.serializer.part import PartSerializer
from rest_framework.pagination import PageNumberPagination
from project.serializer.project import ProjectLiteSerializer, ProjectSerializer, ProjectSummarySerializer, ProjectVendorSummarySerializer
from django.db.models import Count, Q
from django.utils.timezone import now
from datetime import datetime

from users.models import UserProfile

class MRDGroupedPagination(PageNumberPagination):
    page_size = 10  # Number of groups per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProjectPagination(PageNumberPagination):
    page_size = 100  # Number of projects per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProjectView(APIView):
    def get(self, request):
        project_no = request.query_params.get('project_no')
        mrd = request.query_params.get('mrd')
        if not project_no:
            return Response({'error':True,'error_message': 'Project number is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            user_vendors = user_profile.vendor.all().values_list('name', flat=True)
            if mrd:
                parts = Part.objects.filter(project__project_no=project_no, qr_code_scanning__in=user_vendors, mrd=mrd)
            else :
                parts = Part.objects.filter(project__project_no=project_no, qr_code_scanning__in=user_vendors)
            if len(parts) == 0:
                    return Response({'error':True,'error_message': f'{project_no} - Project not found .'}, status=status.HTTP_404_NOT_FOUND)

            project = Project.objects.get(project_no=project_no)
            
        except Project.DoesNotExist:
            return Response({'error':True,'error_message': f'{project_no} - Project not found .'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProjectLiteSerializer(project)
        partSerializer = PartSerializer(parts, many=True)
        response_data = serializer.data
        response_data['parts'] = partSerializer.data
        return Response(response_data, status=status.HTTP_200_OK)


class ProjectListView(APIView):
    def get(self, request):
        project = Project.objects.all().order_by('created_at')
        serializer = ProjectSerializer(project, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectListFilterView(APIView):
    def get(self, request):
        project_no = request.query_params.get('project_no')
        project = Project.objects.filter(project_no__icontains=project_no).order_by('created_at')
        serializer = ProjectSerializer(project, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectListFilterPagenatedView(APIView):
    pagination_class = ProjectPagination
    
    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        user_vendors = user_profile.vendor.all().values_list('name', flat=True)
        project_no = request.query_params.get('project_no')
        project_ids = Part.objects.filter(qr_code_scanning__in=user_vendors, 
                                          project__project_no__icontains=project_no).values_list('project_id', flat=True).distinct()
        projects = Project.objects.filter(id__in=project_ids).order_by('created_at')


        # projects = Project.objects.filter(project_no__icontains=project_no).order_by('created_at')

        paginator = self.pagination_class()
        paginated_projects = paginator.paginate_queryset(projects, request)
        
        # Serialize paginated project data only
        project_serializer = ProjectLiteSerializer(paginated_projects, many=True)
        
        return paginator.get_paginated_response(project_serializer.data)
    

class ProjectListMRDFilterPagenatedView(APIView):
    pagination_class = MRDGroupedPagination
    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        user_vendors = user_profile.vendor.all().values_list('name', flat=True)
        mrd = request.query_params.get('mrd', '').strip()  # Fetch the mrd value from the request
        project_no = request.query_params.get('project_no', '').strip()  # Fetch the mrd value from the request
        type = request.query_params.get('type', 'all').strip()  # Fetch the mrd value from the request

        if not mrd and not project_no:
            return Response({"error": "MRD date or Project No is required."}, status=400)

        if not project_no:
            parts = Part.objects.filter(
                Q(status=Part.Status.MovedToVendor.value) & Q(mrd__icontains=mrd) & Q(qr_code_scanning__in=user_vendors)
            ).order_by('mrd').select_related('project')
        elif not mrd:
            parts = Part.objects.filter(
            Q(status=Part.Status.MovedToVendor.value) & Q(project__project_no__icontains=project_no) & Q(qr_code_scanning__in=user_vendors)
            ).order_by('mrd').select_related('project')
        else:
            parts = Part.objects.filter(
            Q(status=Part.Status.MovedToVendor.value) & Q(mrd__icontains=mrd) & Q(project__project_no__icontains=project_no) & Q(qr_code_scanning__in=user_vendors)
            ).order_by('mrd').select_related('project')
        if type == 'new':
            parts = parts.filter(vendor_status = Part.VendorStatus.Pending_for_acceptance.value)
        else: 
            parts = parts.exclude(vendor_status=Part.VendorStatus.Pending_for_acceptance.value)

        grouped_projects = defaultdict(list)
        for part in parts:
            grouped_projects[part.mrd].append(part.project)

        current_date = now().date()
        flattened_projects = []
        for mrd_date, projects in grouped_projects.items():
            mrd_date_obj = datetime.strptime(mrd_date, "%Y-%m-%d").date()
            due_days_remaining = (mrd_date_obj - current_date).days

            for project in set(projects):  # Avoid duplicate projects
                serializer = ProjectVendorSummarySerializer(
                    project,
                    context={
                        'user_vendors': user_vendors,
                        'mrd': mrd_date,
                        'due_days': due_days_remaining,
                    }
                )
                flattened_projects.append(serializer.data)

        # Step 4: Apply pagination
        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(flattened_projects, request)

        return paginator.get_paginated_response(paginated_data)
    


class ProjectListFilterPartStatusView(APIView):
    def get(self, request):
        status_params = request.query_params.get('status')
        projects = Project.objects.filter(part__status=status_params).distinct().order_by('created_at')
        
        # Custom serialization to include only parts with status 0
        result = []
        for project in projects:
            parts = Part.objects.filter(project=project, status=status_params)
            part_serializer = PartSerializer(parts, many=True)
            project_data = ProjectSerializer(project).data
            project_data['parts'] = part_serializer.data
            result.append(project_data)
        
        return Response(result, status=status.HTTP_200_OK)


class  ProjectVendorSummaryView(APIView):
    pagination_class = MRDGroupedPagination
    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        user_vendors = user_profile.vendor.all().values_list('name', flat=True)
        type = request.query_params.get('type')

        if type == 'new':
            parts = Part.objects.filter(
                Q(status=Part.Status.MovedToVendor.value) & Q(qr_code_scanning__in=user_vendors) & Q(vendor_status=Part.VendorStatus.Pending_for_acceptance.value)
            ).order_by('mrd').select_related('project')
            pending_for_acceptance=True
        else:
            parts = Part.objects.filter(
                Q(status=Part.Status.MovedToVendor.value) & Q(qr_code_scanning__in=user_vendors) & Q(vendor_status__gte=Part.VendorStatus.Pending.value)
            ).order_by('mrd').select_related('project')
            pending_for_acceptance=False

        current_date = now().date()

        if type == 'overdue': 
            filtered_parts = []
            for part in parts:
                try:
                    mrd_date = datetime.strptime(part.mrd, "%Y-%m-%d").date()
                    if mrd_date >= current_date:
                        continue  # Skip non-overdue parts
                    filtered_parts.append(part)
                except ValueError:
                    continue 
        else :
            filtered_parts = parts
        grouped_projects = defaultdict(list)
        for part in filtered_parts:
            print(part.pk)
            print(part.mrd)
            grouped_projects[part.mrd].append(part.project)
        
        flattened_projects = []
        for mrd_date, projects in grouped_projects.items():
            if mrd_date is None: continue
            mrd_date_obj = datetime.strptime(mrd_date, "%Y-%m-%d").date()
            due_days_remaining = (mrd_date_obj - current_date).days

            for project in set(projects):  # Avoid duplicate projects
                serializer = ProjectVendorSummarySerializer(
                    project,
                    context={
                        'user_vendors': user_vendors,
                        'mrd': mrd_date,
                        'due_days': due_days_remaining,
                        'pending_for_acceptance': pending_for_acceptance
                    }
                )
                flattened_projects.append(serializer.data)


        # Step 4: Apply pagination
        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(flattened_projects, request)

        return paginator.get_paginated_response(paginated_data)


class  ProjectNewlyAddedVendorSummaryView(APIView):
    pagination_class = MRDGroupedPagination
    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        user_vendors = user_profile.vendor.all().values_list('name', flat=True)
        parts = Part.objects.filter(
            Q(status=Part.Status.MovedToVendor.value) & Q(qr_code_scanning__in=user_vendors) & Q(vendor_status=Part.VendorStatus.Pending_for_acceptance.value)
        ).order_by('mrd').select_related('project')
        current_date = now().date()

        filtered_parts = parts
        grouped_projects = defaultdict(list)
        for part in filtered_parts:
            grouped_projects[part.mrd].append(part.project)
        
        flattened_projects = []
        for mrd_date, projects in grouped_projects.items():
            mrd_date_obj = datetime.strptime(mrd_date, "%Y-%m-%d").date()
            due_days_remaining = (mrd_date_obj - current_date).days

            for project in set(projects):  # Avoid duplicate projects
                serializer = ProjectVendorSummarySerializer(
                    project,
                    context={
                        'user_vendors': user_vendors,
                        'mrd': mrd_date,
                        'due_days': due_days_remaining,
                    }
                )
                flattened_projects.append(serializer.data)


        # Step 4: Apply pagination
        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(flattened_projects, request)

        return paginator.get_paginated_response(paginated_data)



class ProjectSummaryView(APIView):
    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        user_vendors = user_profile.vendor.all().values_list('name', flat=True)
        project_ids = Part.objects.filter(qr_code_scanning__in=user_vendors).values_list('project_id', flat=True).distinct()
        projects = Project.objects.filter(id__in=project_ids).order_by('created_at')
        
        paginator = PageNumberPagination()
        paginator.page_size = 100  # You can override the default page size here
        paginated_projects = paginator.paginate_queryset(projects, request)
        serializer = ProjectSummarySerializer(paginated_projects, many=True,  context={'user_vendors': user_vendors} )
        return paginator.get_paginated_response(serializer.data)

class  ProjectSummaryFilterView(APIView):
    def get(self, request):
        mrd = request.query_params.get('mrd', '').strip()  # Fetch the mrd value from the request
        project_no = request.query_params.get('project_no', '').strip()  # Fetch the mrd value from the request
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        user_vendors = user_profile.vendor.all().values_list('name', flat=True)
        if not project_no:
            project_ids = Part.objects.filter(
                 Q(mrd__icontains=mrd) & Q(qr_code_scanning__in=user_vendors)
            ).values_list('project_id', flat=True).distinct()
        elif not mrd:  
            project_ids = Part.objects.filter(
                 (Q(project__project_no__icontains=project_no) | Q(project__project_name__icontains=project_no)) & Q(qr_code_scanning__in=user_vendors)
            ).values_list('project_id', flat=True).distinct() 
        else:
            project_ids = Part.objects.filter(
                 Q(mrd__icontains=mrd) & Q(qr_code_scanning__in=user_vendors) & (Q(project__project_no__icontains=project_no) | Q(project__project_name__icontains=project_no))
            ).values_list('project_id', flat=True).distinct()
        projects = Project.objects.filter(pk__in=project_ids).order_by('created_at')

        serializer = ProjectSummarySerializer(projects, many=True, context={
            'user_vendors': user_vendors,
            'mrd': mrd,
        })
        return Response(serializer.data, status=status.HTTP_200_OK)

class  ProjectVendorSummaryFilterView(APIView):
    pagination_class = MRDGroupedPagination
    def get(self, request):
        project_no = request.query_params.get('project_no')
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        user_vendors = user_profile.vendor.all().values_list('name', flat=True)
        parts = Part.objects.filter(
            Q(status=Part.Status.MovedToVendor.value) & Q(project__project_no__icontains=project_no) & Q(qr_code_scanning__in=user_vendors)
        ).order_by('mrd').select_related('project')
        grouped_projects = defaultdict(list)
        for part in parts:
            grouped_projects[part.mrd].append(part.project)

        current_date = now().date()
        flattened_projects = []
        for mrd_date, projects in grouped_projects.items():
            mrd_date_obj = datetime.strptime(mrd_date, "%Y-%m-%d").date()
            due_days_remaining = (mrd_date_obj - current_date).days

            for project in set(projects):  # Avoid duplicate projects
                serializer = ProjectVendorSummarySerializer(
                    project,
                    context={
                        'user_vendors': user_vendors,
                        'mrd': mrd_date,
                        'due_days': due_days_remaining,
                    }
                )
                flattened_projects.append(serializer.data)

        # Step 4: Apply pagination
        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(flattened_projects, request)

        return paginator.get_paginated_response(paginated_data)


class ProjectListFilterStatusPagenatedView(APIView):
    pagination_class = ProjectPagination

    def get(self, request):
        status_params = request.GET.getlist('status')
        summary =  request.query_params.get('summary') 
        project_ids = Part.objects.filter(status__in=status_params).values_list('project_id', flat=True).distinct()
        projects = Project.objects.filter(pk__in=project_ids).order_by('created_at')
        
        # Apply pagination
        paginator = self.pagination_class()
        paginated_projects = paginator.paginate_queryset(projects, request)
 
        # Serialize paginated project data only
        if summary == '1':
            project_serializer = ProjectSummarySerializer(paginated_projects, many=True)
        else:
            project_serializer = ProjectLiteSerializer(paginated_projects, many=True)
        
        return paginator.get_paginated_response(project_serializer.data)
    

class ProjectListWithCountView(APIView):
    pagination_class = ProjectPagination

    def get(self, request):
        status_params = request.GET.getlist('status')    
        project_ids = Part.objects.filter(status__in=status_params).values_list('project_id', flat=True).distinct()
        projects = Project.objects.filter(pk__in=project_ids).order_by('created_at')
        
        # Apply pagination
        paginator = self.pagination_class()
        paginated_projects = paginator.paginate_queryset(projects, request)
        
        # Serialize paginated project data only
        project_serializer = ProjectSummarySerializer(paginated_projects, many=True)
        
        return paginator.get_paginated_response(project_serializer.data)

class ProjectListFilterPartStatusAndProjectIdView(APIView):
    def get(self, request):
        status_list = request.GET.getlist('status')
        id = request.query_params.get('projectId')
        type = request.query_params.get('type')
        projects = Project.objects.filter(pk=id,part__status__in=status_list).distinct().order_by('created_at')
        
        # Custom serialization to include only parts with status 0
        result = []
        for project in projects:
            if type == 'qcFailed':
                parts = Part.objects.filter(project=project, status__in=status_list,qc_passed=False, vendor_status=Part.VendorStatus.Recieved_In_Factory.value)
            elif type == 'goodsReceipt':
                parts = Part.objects.filter(project=project, status__in=status_list, vendor_status=Part.VendorStatus.Recieved_In_Factory.value)
            else :
                parts = Part.objects.filter(project=project, status__in=status_list)
            part_serializer = PartSerializer(parts, many=True)
            project_data = ProjectSerializer(project).data
            project_data['parts'] = part_serializer.data
            result.append(project_data)
        
        return Response(result, status=status.HTTP_200_OK)
    