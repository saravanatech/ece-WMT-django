from rest_framework import serializers

from project.models.ebom import Ebom

class EbomSerializer(serializers.ModelSerializer):

    customerName = serializers.CharField(source='customer_name')
    groupCode = serializers.CharField(source='group_code')
    partDescription = serializers.CharField(source='part_description')
    partNumber = serializers.CharField(source='part_number')
    productType = serializers.CharField(source='product_type')
    projectName = serializers.CharField(source='project_name')
    projectNo = serializers.CharField(source='project_no')
    poMoNo = serializers.CharField(source='po_mo_no', required=False, allow_blank=True)
    remarks = serializers.CharField()


    class Meta:
        model = Ebom
        fields = ['customerName', 'groupCode', 'partDescription', 'partNumber',
                  'productType', 'projectName', 'projectNo', 'qty', 'uom', 'poMoNo', 'remarks']
        read_only_fields = ['created_at', 'updated_at']
