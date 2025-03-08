from django.db import models
from enum import Enum
from django.contrib.auth.models import User

class Project(models.Model):

    customer_name = models.CharField(max_length=255, db_index=True, null=False, blank=False)
    product_type = models.CharField(max_length=100)
    project_name = models.CharField(max_length=255, db_index=True, null=False, blank=False)
    project_no = models.CharField(max_length=100, db_index=True, null=False, blank=False)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_shipped_time = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, db_index=True, blank=True, null=True, related_name='created_by_user')
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, db_index=True, blank=True, null=True, related_name='updated_by_user')
   

    def __str__(self):
        return str(self.project_no)
