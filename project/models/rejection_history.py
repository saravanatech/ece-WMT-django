from django.db import models
from django.contrib.auth.models import User
from masters.models.vendor import VendorMasters
from project.models.parts import Part
from django.utils import timezone

class VendorRejectionHistory(models.Model):
    part = models.ForeignKey(Part,on_delete=models.CASCADE, db_index=True, related_name='rejection_history')
    vendor = models.ForeignKey(VendorMasters,  on_delete=models.CASCADE, db_index=True, null=True, blank=True)
    mrd = models.CharField(max_length=20, blank=True, null=True)
    assigned_on = models.DateTimeField(default=timezone.now(),blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, db_index=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.part.part_description

