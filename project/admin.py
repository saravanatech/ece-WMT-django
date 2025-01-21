from django.contrib import admin

from project.models.ebom import Ebom
from project.models.package_index import PackageIndex
from project.models.part_log import PartLog
from project.models.parts import Part
from project.models.project import Project
from project.models.rejection_history import VendorRejectionHistory
from project.models.vehicle import Vehicle

# Register your models here.
class EbomAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = [f.name for f in Ebom._meta.fields]

admin.site.register(Ebom, EbomAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = [f.name for f in Project._meta.fields]
    search_fields = ['project_name','project_no']
    list_filter = ['status', 'product_type']

admin.site.register(Project, ProjectAdmin)


class VendorRejectionHistoryAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = [f.name for f in VendorRejectionHistory._meta.fields]
    search_fields = ['part__part_description','part__part_number']
    list_filter = ['vendor']

admin.site.register(VendorRejectionHistory, VendorRejectionHistoryAdmin)

class PartAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = [f.name for f in Part._meta.fields]
    search_fields=['project__project_name', 'project__project_no', 'group_code','po_mo_no', 'package_name', 'part_number','part_description']
    list_filter= ['vendor_status', 'status', 'vehicle_status']

admin.site.register(Part, PartAdmin)


class PartLogAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = [f.name for f in PartLog._meta.fields]
    search_fields=['project__project_name', 'project__project_no', 'part__group_code','part__po_mo_no', 'part__package_name', 'part__part_number','part__part_description']

admin.site.register(PartLog, PartLogAdmin)


class PackageIndexAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = [f.name for f in PackageIndex._meta.fields]

admin.site.register(PackageIndex, PackageIndexAdmin)

class VehicleAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = [f.name for f in Vehicle._meta.fields]
    search_fields = ['truck_no']

admin.site.register(Vehicle, VehicleAdmin)