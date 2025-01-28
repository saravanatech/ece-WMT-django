from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from masters.models.product_group import ProductGroupMaster
from masters.models.product_group_package import ProductGroupPackageMaster
from project.models.parts import Part
from project.models.project import Project
from project.serializer.ebom import EbomSerializer

class EbomUploadView(APIView):
    def post(self, request):
        serializer = EbomSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            for item in serializer.data:
                project_no = item.get('projectNo')
                project, _ = Project.objects.get_or_create(project_no=project_no)
                project.customer_name = item.get('customerName')
                project.product_type = item.get('productType')
                project.project_name = item.get('projectName')
                project.created_by =self.request.user
                project.updated_by = self.request.user
                project.save()

                part, created = Part.objects.get_or_create(project=project,part_number=item.get('partNumber'),group_code=item.get('groupCode'))
                if(created) :
                    part.group_code = item.get('groupCode')
                    part.part_description = item.get('partDescription')
                    part.po_mo_no = item.get('poMoNo')
                    part.qty = item.get('qty', 1)
                    part.uom = item.get('uom')
                    part.created_by = self.request.user
                    part.updated_by = self.request.user
                    part.save()


                    product_grouping = ProductGroupMaster.objects.filter(product=project.product_type, group_code = part.group_code)[0]
                    if product_grouping :
                        part.package_name = product_grouping.packing_name
                        part.fixed_variable = product_grouping.fixed 
                        part.no_of_packages = product_grouping.no_of_packages
                        part.wht_team_name = product_grouping.wh_team_name
                        part.source_of_supply = product_grouping.source_of_supply
                        part.qr_type = product_grouping.qr_type
                        part.qr_code_scanning = product_grouping.qr_code_scanning
                        part.use_qr_code_scanning = product_grouping.use_qr_code_scanning
                        part.is_po_mo_mandatory = product_grouping.is_po_mo_mandatory
                        part.po_mo_no = part.po_mo_no if part.is_po_mo_mandatory else ''
                        part.no_of_packages = product_grouping.no_of_packages
                        print(part.group_code)

                        print(part.no_of_packages)
                        part.save()   

                    product_grouping_package = ProductGroupPackageMaster.objects.filter(product=project.product_type, group_code = part.group_code, qty=part.qty)
                    if len(product_grouping_package) > 0:
                        part.no_of_packages = product_grouping_package[0].no_of_packages
                        part.save()      

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
