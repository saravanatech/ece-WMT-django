from project.models.package_index import PackageIndex
from project.models.project import Project


def fetchPackingSlipQRCodeDetails(qr_data):
    type = qr_data.get('t', '')
    if 'ps' in type:
        return fetchPackingSlipForShortQRCodeDetails(qr_data)
    else:
        package_name = qr_data['packageName']
        project_no = qr_data['projectNo']
        package_index = qr_data['packageIndex']
        revision = qr_data['r']
        
        return PackageIndex.objects.filter(
            packageName=package_name,
            ProjectNo=project_no, 
            revision=revision, 
            packAgeIndex=package_index)


#   {"c":"Case-H2,C1311A,42,1,1","t":"ps"}
#   {
#   "c":"<packageName>,<GroupdCode>,<project Id>,<Package Index>,<revision no>",
#   "t":"ps"
#   }
def fetchPackingSlipForShortQRCodeDetails(qr_data):
    content = qr_data['c']
    content_split = content.split(',')
    package_name = content_split[0]
    groupd_code = content_split[1]
    project_id = content_split[2]
    package_index = content_split[3]
    revision = content_split[4]

    try :
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return
    type = qr_data.get('t', None)

    if type == 'ps2':
        return PackageIndex.objects.filter(
                part__group_code=groupd_code,
                packageName=package_name,
                ProjectNo=project.project_no, 
                revision=revision, 
                packAgeIndex=package_index)
    else :
        return PackageIndex.objects.filter(
            packageName=package_name,
            ProjectNo=project.project_no, 
            revision=revision, 
            packAgeIndex=package_index)