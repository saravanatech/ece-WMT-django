from django.db import models
from django import forms
from django.contrib.auth.models import User
from enum import Enum

class Batch(models.Model):
    class Status(Enum):
        Draft = 0
        ItemsUploaded = 1
        Completed = 10
        AllItemsQRGenerated = 20
        Cancelled = 30
        
    batch_no = models.CharField(max_length=100, db_index=True)
    date = models.DateField(max_length=50, blank=False, null=True, db_index=True) 
    status = models.IntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True,null=True, db_index=True, related_name='fo_created_by')
    updated_by =  models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='fo_updated_by')

    def __str__(self):  # __unicode__ on Python 2
        return str(self.batch_no)