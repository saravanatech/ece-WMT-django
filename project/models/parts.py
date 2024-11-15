from enum import Enum
from django.db import models

from masters.models.product_group import ProductGroupMaster
from masters.models.vendor import VendorMasters
from project.models.project import Project
from django.contrib.auth.models import User
from rest_framework import serializers

from project.models.vehicle import Vehicle


class Part(models.Model):
    class Status(Enum):
        InQueue = 0
        Approved = 1
        MovedToVendor = 2
        PartiallyLoaded = 3
        Delivered = 10

    class VechileStatus(Enum):
        NoTruckData = 0
        TrukDataLoaded = 1
        PartiallyLoaded = 2
        UnLoaded = 3
        LoadedInTruck = 4
    
    class DistributionVehicleStatus(Enum):
        NoTruckData = 0
        TrukDataLoaded = 1
        PartiallyLoaded = 2
        UnLoaded = 3
        LoadedInTruck = 4
        
    class VendorStatus(Enum):
        Pending = 0
        QR_Generated = 1
        package_allocation_done = 2
        Packing_Slip_Generated = 3
    
    project = models.ForeignKey(Project,  on_delete=models.CASCADE, db_index=True)
    group_code = models.CharField(max_length=50, db_index=True, null=False, blank=False)
    part_description = models.CharField(max_length=255)
    part_number = models.CharField(max_length=100, db_index=True)
    qty = models.IntegerField(default=1,)
    uom = models.CharField(max_length=50, blank=True, null=True)
    po_mo_no = models.CharField(max_length=100, blank=True, null=True)
    vendor = models.ForeignKey(VendorMasters, db_index=True, null=True, blank=True, on_delete=models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, db_index=True, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="vehicle_part")
    distribution_vehicle = models.ForeignKey(Vehicle, db_index=True, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="distributon_vehicle_part")
    package_name = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    fixed_variable = models.CharField(max_length=3, default='F')
    no_of_packages = models.CharField(max_length=100, default='1')
    wht_team_name = models.CharField(max_length=100, default='', blank=True, null=True)
    source_of_supply = models.CharField(max_length= 100, blank=True, null=True)
    mrd =  models.CharField(max_length= 100, blank=True, null=True)
    revised_mrgd = models.CharField(max_length= 100, blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, db_index=True, blank=True, null=True, related_name='created_by')
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, db_index=True, blank=True, null=True, related_name='updated_by')
    truck_type =  models.CharField(max_length= 100, blank=True, null=True)
    truck_no = models.CharField(max_length= 100, blank=True,null=True, db_index=True)
    bay_in = models.CharField(max_length= 100, blank=True,null=True)
    bay_out = models.CharField(max_length= 100, blank=True,null=True)
    tat = models.CharField(max_length= 100, blank=True,null=True)
    qr_type = models.CharField(max_length=50, db_index=True, default='Type-1')
    
    status = models.IntegerField(default=0)
    distribution_vehicle_status = models.IntegerField(default=0)
    vendor_status = models.IntegerField(default=0)
    vehicle_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    qr_data = models.TextField(max_length=500,blank=True, null=True)
    is_ecn = models.BooleanField(default=False, db_index=True, blank=True, null=True)
    load_in_truck_time = models.DateTimeField(blank=True, null=True)
    part_package_mapping = models.TextField(max_length=800, default='', blank=True, null=True)
    use_qr_code_scanning = models.BooleanField(default=False)
    qr_code_scanning = models.CharField(max_length=100,default='', blank=True, null=True)
    scanned_packages = models.CharField(max_length=50, blank=True, null=True, default='')
    is_po_mo_mandatory = models.BooleanField(default=False, db_index=True, blank=True, null=True)



    def __str__(self):
        return str(self.project.project_no+" - "+self.part_number+" - "+ self.group_code) 
    
    class Meta:
        unique_together = ('project', 'part_number','group_code')
