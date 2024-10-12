from rest_framework import serializers
from first_operation.models.rm_code_master import RMCodeMaster


class RMCodeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        """
        """
        model = RMCodeMaster
        fields = "__all__"
