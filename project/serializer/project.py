from rest_framework import serializers

from project.models.ebom import Ebom
from project.models.parts import Part
from project.models.project import Project
from project.serializer.activity_log import ActivityLogSerializer
from project.serializer.part import PartSerializer

class ProjectSerializer(serializers.ModelSerializer):

    customerName = serializers.CharField(source='customer_name')
    productType = serializers.CharField(source='product_type')
    projectName = serializers.CharField(source='project_name')
    projectNo = serializers.CharField(source='project_no')
    createdAt = serializers.CharField(source='created_at')
    updatedAt = serializers.CharField(source='updated_at')

    parts = PartSerializer(many=True, read_only=True, source='part_set')
    activityLogs = ActivityLogSerializer(many=True, read_only=True, source='activity_logs')


    class Meta:
        model = Project
        fields = ['customerName',
                  'productType', 'projectName', 'projectNo','status', 'parts', 'updatedAt', 'createdAt', 'activityLogs']
        read_only_fields = ['created_at', 'updated_at']



class ProjectSummarySerializer(serializers.ModelSerializer):

    customerName = serializers.CharField(source='customer_name')
    productType = serializers.CharField(source='product_type')
    projectName = serializers.CharField(source='project_name')
    projectNo = serializers.CharField(source='project_no')
    total_parts_count = serializers.SerializerMethodField()
    count_of_packingSlip_generated = serializers.SerializerMethodField()
    count_of_delivered = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['customerName',
                  'productType', 'projectName', 'projectNo', 'total_parts_count', 'count_of_packingSlip_generated', 'count_of_delivered']

    def get_total_parts_count(self, obj):
        return Part.objects.filter(project=obj).count()

    def get_count_of_packingSlip_generated(self, obj):
        return Part.objects.filter(project=obj, vendor_status=Part.VendorStatus.Packing_Slip_Generated.value).count()

    def get_count_of_delivered(self, obj):
        return Part.objects.filter(project=obj, vehicle_status=Part.VechileStatus.LoadedInTruck.value).count()
