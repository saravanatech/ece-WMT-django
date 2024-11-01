from django.db import models
from django import forms
from django.contrib.auth.models import User
from enum import Enum

from first_operation.models.batch import Batch

class BatchItems(models.Model):
    class Status(Enum):
        Draft = 1
        Completed = 10
        QRGenerated = 20
        Cancelled = 30
        
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE, null=True, db_index=True, related_name='batch_items_set')
    status = models.IntegerField(default=0, db_index=True)
    rm_code = models.CharField(max_length=100, db_index=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    thickness = models.CharField(max_length=25)
    item_code= models.CharField(max_length=100, db_index=True)
    qty = models.IntegerField(default=0)
    sheet_thickness  =  models.CharField(max_length=10)
    material = models.CharField(max_length=255, db_index=True)
    nesting_count =  models.IntegerField(default=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True,null=True, db_index=True, related_name='fo_bi_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, db_index=True, related_name='fo_bi_updated_by')
    error = models.BooleanField(default=False)
    error_message = models.CharField(max_length=255, db_index=True)
    repeating_qty = models.IntegerField(default=1, null=True, blank=True)


    def __str__(self):  # __unicode__ on Python 2
        return str(self.rm_code)