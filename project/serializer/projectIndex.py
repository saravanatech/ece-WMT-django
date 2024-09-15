from rest_framework import serializers

from project.models.package_index import PackageIndex
from project.models.part_log import PartLog

class PackageIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageIndex
        fields = '__all__'