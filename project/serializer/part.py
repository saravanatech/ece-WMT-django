from rest_framework import serializers

from masters.models.product_group import ProductGroupMaster
from project.models.parts import Part
from project.serializer.activity_log import ActivityLogSerializer
from project.serializer.part_log import PartLogSerializer

class PartSerializer(serializers.ModelSerializer):

    projectNo = serializers.CharField(source='project.project_no')
    groupCode = serializers.CharField(source='group_code')
    partDescription = serializers.CharField(source='part_description')
    partNumber = serializers.CharField(source='part_number')
    poMoNo = serializers.CharField(source='po_mo_no', allow_blank=True, allow_null=True)
    vendor = serializers.CharField(source='vendor.name', allow_blank=True, allow_null=True)
    
    packageName = serializers.CharField(source='package_name', allow_blank=True, allow_null=True)
    fixedVariable = serializers.CharField(source='fixed_variable')
    noOfPackages = serializers.CharField(source='no_of_packages')
    whtTeamName = serializers.CharField(source='wht_team_name')
    sourceOfSupply = serializers.CharField(source='source_of_supply', allow_blank=True, allow_null=True)
    revisedMrgd = serializers.CharField(source='revised_mrgd', allow_blank=True, allow_null=True)
    truckType = serializers.CharField(source='truck_type', allow_blank=True, allow_null=True)
    truckNo = serializers.CharField(source='truck_no', allow_blank=True, allow_null=True)
    bayIn = serializers.CharField(source='bay_in', allow_blank=True, allow_null=True)
    bayOut = serializers.CharField(source='bay_out', allow_blank=True, allow_null=True)
    qrType = serializers.CharField(source='qr_type', allow_blank=True, allow_null=True)
    createdBy = serializers.CharField(source='created_by.username', allow_blank=True, allow_null=True)
    updatedBy = serializers.CharField(source='updated_by.username', allow_blank=True, allow_null=True)
    vendorStatus = serializers.IntegerField(source='vendor_status')
    partPackageMapping = serializers.CharField(source='part_package_mapping', allow_blank=True, allow_null=True)
    vehicleStatus = serializers.IntegerField(source='vehicle_status')
    qrData = serializers.CharField(source='qr_data', allow_blank=True, allow_null=True)
    isEcn = serializers.BooleanField(source='is_ecn', default=False)
    availableVendors = serializers.SerializerMethodField()
    useQRCodeScanning = serializers.BooleanField(source='use_qr_code_scanning', default=False)
    isPoMoMandatory = serializers.BooleanField(source='is_po_mo_mandatory', default=False)
    QRCodeScanning = serializers.CharField(source='qr_code_scanning', allow_blank=True, allow_null=True)
    scannedPackages=serializers.CharField(source='scanned_packages', allow_blank=True, allow_null=True)
    partLogs = PartLogSerializer(many=True, read_only=True, source='part_logs')




    class Meta:
        model = Part
        fields = [
            'id','projectNo', 'groupCode', 'partDescription', 'partNumber',
            'qty', 'uom', 'poMoNo', 'vendor','vehicleStatus', 'useQRCodeScanning', 'QRCodeScanning',
            'fixedVariable', 'packageName','qrData', 'isEcn', 'partPackageMapping', 'scannedPackages',
            'noOfPackages', 'whtTeamName', 'sourceOfSupply', 'mrd', 'revisedMrgd', 'isPoMoMandatory',
            'truckType', 'truckNo', 'bayIn', 'bayOut', 'tat', 'qrType', 'vendorStatus',
            'createdBy', 'updatedBy', 'status', 'created_at', 'updated_at', 'availableVendors',
            'partLogs','vehicle'
        ]

    def update(self, instance, validated_data):
        # Update fields without dotted sources directly
        instance.part_description = validated_data.get('part_description', instance.part_description)
        instance.part_number = validated_data.get('part_number', instance.part_number)
        instance.po_mo_no = validated_data.get('po_mo_no', instance.po_mo_no)
        instance.package_name = validated_data.get('package_name', instance.package_name)
        instance.fixed_variable = validated_data.get('fixed_variable', instance.fixed_variable)
        instance.no_of_packages = validated_data.get('no_of_packages', instance.no_of_packages)
        instance.wht_team_name = validated_data.get('wht_team_name', instance.wht_team_name)
        instance.source_of_supply = validated_data.get('source_of_supply', instance.source_of_supply)
        instance.mrd = validated_data.get('mrd', instance.revised_mrgd)
        instance.revised_mrgd = validated_data.get('revised_mrgd', instance.revised_mrgd)
        instance.truck_type = validated_data.get('truck_type', instance.truck_type)
        instance.vendor_status = validated_data.get('vendor_status', instance.vendor_status)
        instance.truck_no = validated_data.get('truck_no', instance.truck_no)
        instance.bay_in = validated_data.get('bay_in', instance.bay_in)
        instance.bay_out = validated_data.get('bay_out', instance.bay_out)
        instance.qr_type = validated_data.get('qr_type', instance.qr_type)
        instance.qty = validated_data.get('qty', instance.qty)
        instance.uom = validated_data.get('uom', instance.uom)
        instance.tat = validated_data.get('tat', instance.tat)
        instance.qr_data = validated_data.get('qr_data', instance.qr_data)
        instance.status = validated_data.get('status', instance.status)
        instance.is_ecn = validated_data.get('is_ecn', instance.is_ecn)
        instance.vehicle_status = validated_data.get('vehicle_status', instance.vehicle_status)
        instance.qr_code_scanning = validated_data.get('qr_code_scanning', instance.qr_code_scanning)
        instance.use_qr_code_scanning = validated_data.get('use_qr_code_scanning', instance.use_qr_code_scanning)
        instance.scanned_packages = validated_data.get('scanned_packages', instance.scanned_packages)
        instance.is_po_mo_mandatory = validated_data.get('is_po_mo_mandatory', instance.is_po_mo_mandatory)

        # Save the updated instance
        instance.save()

        return instance

    def get_availableVendors(self, obj):
        try :
            project_grouping = ProductGroupMaster.objects.get(product=obj.project.product_type, group_code = obj.group_code)
            vendors = project_grouping.vendors.all()
            vendor_names = [vendor.name for vendor in vendors]  # Extract names
            return vendor_names
        except Exception as e:
            return []
