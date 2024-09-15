from django.db import models

from django.contrib.auth.models import User

from project.models.vehicle import Vehicle

class VehicleLog(models.Model):
    vechile= models.ForeignKey(Vehicle, null=False, blank=False, on_delete=models.CASCADE)
    logMessage = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=50, default='info', blank=True, null=True)
    created_by = models.ForeignKey(User,  on_delete=models.DO_NOTHING, db_index=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vechile.truck_no
