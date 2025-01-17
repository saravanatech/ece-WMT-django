from project.models.package_index import PackageIndex


def fetchPackingSlipQRCodeDetails(qr_data):
    package_name = qr_data['packageName']
    project_no = qr_data['projectNo']
    package_index = qr_data['packageIndex']
    revision = qr_data['r']
      
    return PackageIndex.objects.filter(
        packageName=package_name,
        ProjectNo=project_no, 
        revision=revision, 
        packAgeIndex=package_index)