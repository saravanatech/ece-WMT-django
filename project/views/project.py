from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from project.models import Project
from project.models.parts import Part
from project.serializer.part import PartSerializer
from rest_framework.pagination import PageNumberPagination
from project.serializer.project import ProjectLiteSerializer, ProjectSerializer, ProjectSummarySerializer, ProjectVendorSummarySerializer
from django.db.models import Count, Q

from users.models import UserProfile


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
                parts = Part.objects.filter(project__project_no=project_no, vendor__pk__in=user_vendors, mrd=mrd)
            else :
                parts = Part.objects.filter(project__project_no=project_no, vendor__pk__in=user_vendors)
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
        project_ids = Part.objects.filter(vendor__pk__in=user_vendors, 
                                          project__project_no__icontains=project_no).values_list('project_id', flat=True).distinct()
        projects = Project.objects.filter(id__in=project_ids).order_by('created_at')


        # projects = Project.objects.filter(project_no__icontains=project_no).order_by('created_at')

        paginator = self.pagination_class()
        paginated_projects = paginator.paginate_queryset(projects, request)
        
        # Serialize paginated project data only
        project_serializer = ProjectLiteSerializer(paginated_projects, many=True)
        
        return paginator.get_paginated_response(project_serializer.data)
    

class ProjectListMRDFilterPagenatedView(APIView):
    
    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        user_vendors = user_profile.vendor.all().values_list('name', flat=True)
        mrd = request.query_params.get('mrd', '').strip()  # Fetch the mrd value from the request
        project_no = request.query_params.get('project_no', '').strip()  # Fetch the mrd value from the request

        if not mrd and not project_no:
            return Response({"error": "MRD date or Project No is required."}, status=400)

        if not project_no:
            project_ids = Part.objects.filter(mrd__icontains=mrd, vendor__pk__in=user_vendors).values_list('project_id', flat=True).distinct()
        elif not mrd:
            project_ids = Part.objects.filter(project__project_no__icontains=project_no, vendor__pk__in=user_vendors).values_list('project_id', flat=True).distinct()
        else:
            project_ids = Part.objects.filter(mrd__icontains=mrd, project__project_no__icontains=project_no, vendor__pk__in=user_vendors).values_list('project_id', flat=True).distinct()

        projects = Project.objects.filter(pk__in=project_ids).order_by('created_at')
        # Serialize paginated project data only
        serializer = ProjectVendorSummarySerializer(projects, many=True,  context={'user_vendors': user_vendors, 'mrd': mrd} )
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    


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


class ProjectVendorSummaryView(APIView):
    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        user_vendors = user_profile.vendor.all().values_list('name', flat=True)
        project_ids = Part.objects.filter(vendor__pk__in=user_vendors, status=Part.Status.MovedToVendor.value).values_list('project_id', flat=True).distinct()
        projects = Project.objects.filter(id__in=project_ids).order_by('created_at')

        paginator = PageNumberPagination()
        paginator.page_size = 100  # You can override the default page size here
        paginated_projects = paginator.paginate_queryset(projects, request)
        serializer = ProjectVendorSummarySerializer(paginated_projects, many=True,  context={'user_vendors': user_vendors} )
        return paginator.get_paginated_response(serializer.data)


class ProjectSummaryView(APIView):
    def get(self, request):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        user_vendors = user_profile.vendor.all().values_list('name', flat=True)
        project_ids = Part.objects.filter(vendor__pk__in=user_vendors).values_list('project_id', flat=True).distinct()
        projects = Project.objects.filter(id__in=project_ids).order_by('created_at')
        
        paginator = PageNumberPagination()
        paginator.page_size = 100  # You can override the default page size here
        paginated_projects = paginator.paginate_queryset(projects, request)
        serializer = ProjectSummarySerializer(paginated_projects, many=True,  context={'user_vendors': user_vendors} )
        return paginator.get_paginated_response(serializer.data)

class  ProjectVendorSummaryFilterView(APIView):
    def get(self, request):
        project_no = request.query_params.get('project_no')
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        user_vendors = user_profile.vendor.all().values_list('name', flat=True)
        project_ids = Part.objects.filter(project__project_no__icontains=project_no, vendor__pk__in=user_vendors).values_list('project_id', flat=True).distinct()
        projects = Project.objects.filter(pk__in=project_ids).order_by('created_at')

        serializer = ProjectVendorSummarySerializer(projects, many=True, context={'user_vendors': user_vendors})
        return Response(serializer.data, status=status.HTTP_200_OK)

class  ProjectSummaryFilterView(APIView):
    def get(self, request):
        project_no = request.query_params.get('project_no')
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        user_vendors = user_profile.vendor.all().values_list('name', flat=True)
        project_ids = Part.objects.filter(project__project_no__icontains=project_no).values_list('project_id', flat=True).distinct()
        projects = Project.objects.filter(pk__in=project_ids).order_by('created_at')

        serializer = ProjectSummarySerializer(projects, many=True, context={'user_vendors': user_vendors})
        return Response(serializer.data, status=status.HTTP_200_OK)




class ProjectListFilterStatusPagenatedView(APIView):
    pagination_class = ProjectPagination

    def get(self, request):
        status_params = request.GET.getlist('status')    
        project_ids = Part.objects.filter(status__in=status_params).values_list('project_id', flat=True).distinct()
        projects = Project.objects.filter(pk__in=project_ids).order_by('created_at')
        
        # Apply pagination
        paginator = self.pagination_class()
        paginated_projects = paginator.paginate_queryset(projects, request)
        
        # Serialize paginated project data only
        project_serializer = ProjectLiteSerializer(paginated_projects, many=True)
        
        return paginator.get_paginated_response(project_serializer.data)
    

class ProjectListFilterPartStatusAndProjectIdView(APIView):
    def get(self, request):
        status_list = request.GET.getlist('status')
        id = request.query_params.get('projectId')
        projects = Project.objects.filter(pk=id,part__status__in=status_list).distinct().order_by('created_at')
        
        # Custom serialization to include only parts with status 0
        result = []
        for project in projects:
            parts = Part.objects.filter(project=project, status__in=status_list)
            part_serializer = PartSerializer(parts, many=True)
            project_data = ProjectSerializer(project).data
            project_data['parts'] = part_serializer.data
            result.append(project_data)
        
        return Response(result, status=status.HTTP_200_OK)