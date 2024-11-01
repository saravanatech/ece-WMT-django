from django.db import models
from django import forms
from django.contrib.auth.models import User
from enum import Enum

from first_operation.models.batch import Batch
from first_operation.models.batch_items import BatchItems

class BatchNestingItems(models.Model):
    class Status(Enum):
        Draft = 0
        Completed = 10
        qrGenerated = 20
        Cancelled = 30

    nesting_item_code =  models.CharField(max_length=100, db_index=True)
    nesting_number = models.CharField(max_length=50, db_index=True, null=False, blank=False, default="N1")
    batch_items = models.ForeignKey(BatchItems, on_delete=models.CASCADE, db_index=True, related_name='batch_items')
    item_qty = models.IntegerField(default=1)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='fo_bni_created_by')
    updated_by =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='fo_bni_updated_by')
    status = models.IntegerField(default=0)
    material =  models.CharField(max_length=100, db_index=True)
    sheetThickness =  models.CharField(max_length=100, db_index=True)
    batchNo =  models.CharField(max_length=100, db_index=True)

        
    def __str__(self): 
        return str(self.nesting_item_code)