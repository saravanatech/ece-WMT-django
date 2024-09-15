from django.db import models
from enum import Enum
from django.contrib.auth.models import User

class Vehicle(models.Model):
    class Status(Enum):
        Active = 0
        Shipped = 1
        Canceled = 2

    truck_no = models.CharField(max_length=255, db_index=True, null=False, blank=False)
    truck_type = models.CharField(max_length=100, null=True, blank=False)
    status = models.IntegerField(default=0)
    bay_in_time = models.DateTimeField(null=True, blank=True)
    bay_out_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, db_index=True, blank=True, null=True, related_name='vehicle_created_by_user')
    updated_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, db_index=True, blank=True, null=True, related_name='vehicle_updated_by_user')
   

    def __str__(self):
        return str(self.truck_no)
