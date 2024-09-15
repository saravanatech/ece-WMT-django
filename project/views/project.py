from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from project.models import Project
from project.models.parts import Part
from project.serializer.part import PartSerializer
from project.serializer.project import ProjectSerializer, ProjectSummarySerializer

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
        project = Project.objects.all().order_by('created_at')[:10]
        serializer = ProjectSummarySerializer(project, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectSummaryFilterView(APIView):
    def get(self, request):
        project_no = request.query_params.get('project_no')
        project = Project.objects.filter(project_no__icontains=project_no).order_by('created_at')
        serializer = ProjectSummarySerializer(project, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
