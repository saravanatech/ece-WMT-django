from django.db import models
from django import forms
from django.contrib.auth.models import User
from enum import Enum

from first_operation.models.batch import Batch

class BatchItems(models.Model):
    class Status(Enum):
        Draft = 0
        Completed = 10
        PackingSlipGenerated = 20
        Cancelled = 30
        
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE, null=False, db_index=True)
    status = models.IntegerField(default=0, db_index=True)
    rm_code = models.CharField(max_length=100, db_index=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    thickness = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    item_code= models.CharField(max_length=100, db_index=True)
    qty = models.IntegerField(default=0)
    nesting_no = models.CharField(max_length=50)
    sheet_thickness  =  models.DecimalField(max_digits=5, decimal_places=1, default=0)
    material = models.CharField(max_length=255, db_index=True)
    nesting_count =  models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_index=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_index=True, related_name='updated_by')
    error = models.BooleanField(default=False)
    error_message = models.CharField(max_length=255, db_index=True)


    def __str__(self):  # __unicode__ on Python 2
        return str(self.batch_no)