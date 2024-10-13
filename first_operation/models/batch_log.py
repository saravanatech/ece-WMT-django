from django.db import models
from django.contrib.auth.models import User
from first_operation.models.batch import Batch

class BatchLog(models.Model):
    log_message =  models.CharField(max_length=255)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, default="info")

        
    def __str__(self): 
        return str(self.log_message)