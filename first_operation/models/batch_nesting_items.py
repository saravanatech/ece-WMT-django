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
        PackingSlipGenerated = 20
        Cancelled = 30

    nesting_item_code =  models.CharField(max_length=100, db_index=True)
    neting_number = models.CharField(max_length=50, db_index=True)
    batch_items = models.ForeignKey(BatchItems, on_delete=models.CASCADE, db_index=True)
    item_qty = models.IntegerField(default=1)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='fo_created_by')
    updated_by =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='fo_updated_by')
    status = models.IntegerField(default=0)
        
    def __str__(self): 
        return str(self.nesting_item_code)