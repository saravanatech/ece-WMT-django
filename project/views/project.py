from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from project.models import Project
from project.models.parts import Part
from project.serializer.part import PartSerializer
from rest_framework.pagination import PageNumberPagination
from project.serializer.project import ProjectLiteSerializer, ProjectSerializer, ProjectSummarySerializer
from django.db.models import Count, Q


class ProjectPagination(PageNumberPagination):
    page_size = 100  # Number of projects per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProjectView(APIView):
    def get(self, request):
        project_no = request.query_params.get('project_no')
        if not project_no:
            return Response({'error':True,'error_message': 'Project number is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            project = Project.objects.get(project_no=project_no)
        except Project.DoesNotExist:
            return Response({'error':True,'error_message': f'{project_no} - Project not found .'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        project_no = request.query_params.get('project_no')
        projects = Project.objects.filter(project_no__icontains=project_no).order_by('created_at')

        paginator = self.pagination_class()
        paginated_projects = paginator.paginate_queryset(projects, request)
        
        # Serialize paginated project data only
        project_serializer = ProjectSerializer(paginated_projects, many=True)
        
        return paginator.get_paginated_response(project_serializer.data)
    


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


class ProjectSummaryView(APIView):
    def get(self, request):
        project = Project.objects.all().order_by('created_at')
        paginator = PageNumberPagination()
        paginator.page_size = 100  # You can override the default page size here
        paginated_projects = paginator.paginate_queryset(project, request)
        serializer = ProjectSummarySerializer(paginated_projects, many=True)
        return paginator.get_paginated_response(serializer.data)


class ProjectSummaryFilterView(APIView):
    def get(self, request):
        project_no = request.query_params.get('project_no')
        project = Project.objects.filter(project_no__icontains=project_no).order_by('created_at')
        serializer = ProjectSummarySerializer(project, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class ProjectListFilterStatusPagenatedView(APIView):
    pagination_class = ProjectPagination

    def get(self, request):
        status_params = request.query_params.get('status')
        
        # Fetch only projects that have at least one part with the specified status
        projects = (
            Project.objects
            .annotate(part_count=Count('part', filter=Q(part__status=status_params)))
            .filter(part_count__gt=0)
            .order_by('created_at')
        )
        
        # Apply pagination
        paginator = self.pagination_class()
        paginated_projects = paginator.paginate_queryset(projects, request)
        
        # Serialize paginated project data only
        project_serializer = ProjectLiteSerializer(paginated_projects, many=True)
        
        return paginator.get_paginated_response(project_serializer.data)
    

class ProjectListFilterPartStatusAndProjectIdView(APIView):
    def get(self, request):
        status_params = request.query_params.get('status')
        id = request.query_params.get('projectId')
        projects = Project.objects.filter(pk=id,part__status=status_params).distinct().order_by('created_at')
        
        # Custom serialization to include only parts with status 0
        result = []
        for project in projects:
            parts = Part.objects.filter(project=project, status=status_params)
            part_serializer = PartSerializer(parts, many=True)
            project_data = ProjectSerializer(project).data
            project_data['parts'] = part_serializer.data
            result.append(project_data)
        
        return Response(result, status=status.HTTP_200_OK)