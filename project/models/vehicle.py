from django.db import models
from enum import Enum
from django.contrib.auth.models import User

class Vehicle(models.Model):
    class Status(Enum):
        Active = 0
        Shipped = 1
        Canceled = 2

    class DestinationId(Enum):
        Project_site = 0
        Distribution_Center = 1

    truck_no = models.CharField(max_length=255, db_index=True, null=False, blank=False)
    truck_type = models.CharField(max_length=100, null=True, blank=False)
    status = models.IntegerField(default=0, help_text=  "0: Active, 1: Shipped, 2: Cancelled")
    bay_in_time = models.DateTimeField(null=True, blank=True)
    bay_out_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    destination = models.IntegerField(default=0, db_index=True,help_text="0: Project Site , 1:  Destination Center")
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, db_index=True, blank=True, null=True, related_name='vehicle_created_by_user')
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, db_index=True, blank=True, null=True, related_name='vehicle_updated_by_user')
   

    def __str__(self):
        destinationStr  = "Site"
        if self.destination == self.DestinationId.Distribution_Center.value:
            destinationStr = "Distribution Center"
        return str(self.truck_no) +" - "+ destinationStr
