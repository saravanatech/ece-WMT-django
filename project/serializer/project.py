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
        fields = ['id','customerName',
                  'productType', 'projectName', 'projectNo','status', 'parts', 'updatedAt', 'createdAt', 'activityLogs']
        read_only_fields = ['created_at', 'updated_at']

class ProjectLiteSerializer(serializers.ModelSerializer):

    customerName = serializers.CharField(source='customer_name')
    productType = serializers.CharField(source='product_type')
    projectName = serializers.CharField(source='project_name')
    projectNo = serializers.CharField(source='project_no')
    createdAt = serializers.CharField(source='created_at')
    updatedAt = serializers.CharField(source='updated_at')

    class Meta:
        model = Project
        fields = ['customerName',
                  'productType', 'projectName', 'projectNo','status', 'updatedAt', 'createdAt', 'id']
        read_only_fields = ['created_at', 'updated_at']


class ProjectSummarySerializer(serializers.ModelSerializer):

    customerName = serializers.CharField(source='customer_name')
    productType = serializers.CharField(source='product_type')
    projectName = serializers.CharField(source='project_name')
    projectNo = serializers.CharField(source='project_no')
    total_parts_count = serializers.SerializerMethodField()
    count_of_packingSlip_generated = serializers.SerializerMethodField()
    count_of_delivered = serializers.SerializerMethodField()
    count_of_goods_received = serializers.SerializerMethodField()
    count_of_qc_failed = serializers.SerializerMethodField()
    count_of_pending_acceptance = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['id','customerName',
                  'count_of_goods_received',
                  'count_of_qc_failed',
                  'productType', 'projectName', 'projectNo', 'total_parts_count', 'count_of_packingSlip_generated', 'count_of_delivered', 'count_of_pending_acceptance']

    def get_total_parts_count(self, obj):
        user_vendors = self.context.get('user_vendors')
        if not user_vendors:
            return Part.objects.filter(project=obj).count()
        mrd = self.context.get('mrd')
        if mrd :
            return  Part.objects.filter(project=obj, qr_code_scanning__in=user_vendors, mrd=mrd).count()
       
        return Part.objects.filter(project=obj, qr_code_scanning__in=user_vendors).count()

    def get_count_of_packingSlip_generated(self, obj):
        user_vendors = self.context.get('user_vendors')
        if not user_vendors:
            return Part.objects.filter(project=obj, vendor_status__gte=Part.VendorStatus.Packing_Slip_Generated.value).count()
        mrd = self.context.get('mrd')
        if mrd :
            return  Part.objects.filter(project=obj, qr_code_scanning__in=user_vendors,vendor_status__gte=Part.VendorStatus.Packing_Slip_Generated.value, mrd=mrd).count()
        return Part.objects.filter(project=obj, qr_code_scanning__in=user_vendors,vendor_status__gte=Part.VendorStatus.Packing_Slip_Generated.value).count()

    def get_count_of_pending_acceptance(self, obj):
        user_vendors = self.context.get('user_vendors')
        if not user_vendors:
            return Part.objects.filter(project=obj, vendor_status=Part.VendorStatus.Pending_for_acceptance.value).count()
        mrd = self.context.get('mrd')
        if mrd :
            return Part.objects.filter(project=obj,qr_code_scanning__in=user_vendors, vendor_status=Part.VendorStatus.Pending_for_acceptance.value,mrd=mrd).count()
        return Part.objects.filter(project=obj,qr_code_scanning__in=user_vendors, vendor_status=Part.VendorStatus.Pending_for_acceptance.value).count()

    def get_count_of_delivered(self, obj):
        user_vendors = self.context.get('user_vendors')
        if not user_vendors:
            return Part.objects.filter(project=obj, vehicle_status=Part.VechileStatus.LoadedInTruck.value).count()
        mrd = self.context.get('mrd')
        if mrd :
            return Part.objects.filter(project=obj,qr_code_scanning__in=user_vendors, vehicle_status=Part.VechileStatus.LoadedInTruck.value,mrd=mrd).count()
        return Part.objects.filter(project=obj,qr_code_scanning__in=user_vendors, vehicle_status=Part.VechileStatus.LoadedInTruck.value).count()

    def get_count_of_goods_received(self, obj):
        user_vendors = self.context.get('user_vendors')
        if not user_vendors:
            return Part.objects.filter(project=obj, vendor_status=Part.VendorStatus.Recieved_In_Factory.value).count()
        mrd = self.context.get('mrd')
        if mrd :
            return Part.objects.filter(project=obj,qr_code_scanning__in=user_vendors, vendor_status=Part.VendorStatus.Recieved_In_Factory.value,mrd=mrd).count()
        return Part.objects.filter(project=obj,qr_code_scanning__in=user_vendors, vendor_status=Part.VendorStatus.Recieved_In_Factory.value).count()

    def get_count_of_qc_failed(self, obj):
        user_vendors = self.context.get('user_vendors')
        if not user_vendors:
            return Part.objects.filter(project=obj, vendor_status=Part.VendorStatus.Recieved_In_Factory.value, qc_passed=False).count()
        mrd = self.context.get('mrd')
        if mrd :
            return Part.objects.filter(project=obj,qr_code_scanning__in=user_vendors, vendor_status=Part.VendorStatus.Recieved_In_Factory.value, qc_passed=False,mrd=mrd).count()
        return Part.objects.filter(project=obj,qr_code_scanning__in=user_vendors, vendor_status=Part.VendorStatus.Recieved_In_Factory.value, qc_passed=False).count()


class ProjectVendorSummarySerializer(serializers.ModelSerializer):

    customerName = serializers.CharField(source='customer_name')
    productType = serializers.CharField(source='product_type')
    projectName = serializers.CharField(source='project_name')
    projectNo = serializers.CharField(source='project_no')
    total_parts_count = serializers.SerializerMethodField()
    count_of_packingSlip_generated = serializers.SerializerMethodField()
    count_of_delivered = serializers.SerializerMethodField()
    mrd_date = serializers.SerializerMethodField()
    due_days_remaning = serializers.SerializerMethodField()
    pending_for_acceptance = serializers.SerializerMethodField()
    count_of_received_in_factory = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['customerName', 'due_days_remaning', 'mrd_date',
                  'productType', 'projectName', 'projectNo', 'total_parts_count',
                 'count_of_packingSlip_generated', 'count_of_delivered', 'pending_for_acceptance', 'count_of_received_in_factory']

    def get_mrd_date(self, obj):
        mrd_date = self.context.get('mrd', None)
        return mrd_date

    def get_due_days_remaning(self, obj):
        due_days = self.context.get('due_days', None)
        return due_days

    def get_pending_for_acceptance(self, obj):
        pending_for_acceptance =  self.context.get('pending_for_acceptance', False)
        return pending_for_acceptance

    def get_total_parts_count(self, obj):
        user_vendors = self.context.get('user_vendors')
        if not user_vendors:
            return Part.objects.filter(project=obj).count()
        mrd = self.context.get('mrd')
        if mrd :
            return  Part.objects.filter(project=obj, qr_code_scanning__in=user_vendors, status=Part.Status.MovedToVendor.value, mrd=mrd).count()
        return Part.objects.filter(project=obj, qr_code_scanning__in=user_vendors, status=Part.Status.MovedToVendor.value).count()

    def get_count_of_packingSlip_generated(self, obj):
        user_vendors = self.context.get('user_vendors')
        if not user_vendors:
            return Part.objects.filter(project=obj, vendor_status__gte=Part.VendorStatus.Packing_Slip_Generated.value).count()
        mrd = self.context.get('mrd')
        if mrd :
            return Part.objects.filter(project=obj,qr_code_scanning__in=user_vendors,vendor_status__gte=Part.VendorStatus.Packing_Slip_Generated.value,  status=Part.Status.MovedToVendor.value, mrd=mrd).count()
        return Part.objects.filter(project=obj,qr_code_scanning__in=user_vendors,vendor_status__gte=Part.VendorStatus.Packing_Slip_Generated.value,  status=Part.Status.MovedToVendor.value).count()
    
    def get_count_of_received_in_factory(self, obj):
        user_vendors = self.context.get('user_vendors')
        if not user_vendors:
            return Part.objects.filter(project=obj, vendor_status__gte=Part.VendorStatus.Recieved_In_Factory.value).count()
        mrd = self.context.get('mrd')
        if mrd :
            return Part.objects.filter(project=obj,qr_code_scanning__in=user_vendors,vendor_status__gte=Part.VendorStatus.Recieved_In_Factory.value,  status=Part.Status.MovedToVendor.value, mrd=mrd).count()
        return Part.objects.filter(project=obj,qr_code_scanning__in=user_vendors,vendor_status__gte=Part.VendorStatus.Recieved_In_Factory.value,  status=Part.Status.MovedToVendor.value).count()

    def get_count_of_delivered(self, obj):
        user_vendors = self.context.get('user_vendors')
        if not user_vendors:
            return Part.objects.filter(project=obj, vehicle_status=Part.VechileStatus.LoadedInTruck.value).count()
        mrd = self.context.get('mrd')
        if mrd :
            return Part.objects.filter(project=obj,qr_code_scanning__in=user_vendors, vehicle_status=Part.VechileStatus.LoadedInTruck.value,  status=Part.Status.MovedToVendor.value, mrd=mrd).count()
        
        return Part.objects.filter(project=obj,qr_code_scanning__in=user_vendors, vehicle_status=Part.VechileStatus.LoadedInTruck.value,  status=Part.Status.MovedToVendor.value).count()
