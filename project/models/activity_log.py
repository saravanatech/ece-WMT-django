
from django.db import models
from django.contrib.auth.models import User

from project.models.parts import Part
from project.models.project import Project

class ActivityLog(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    project = models.ForeignKey(Project,  on_delete=models.CASCADE, db_index=True, null=True, blank=True, related_name='activity_logs')
    type = models.CharField(max_length=10, default="info")
    project_no = models.CharField(max_length=10, blank=False, null=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Activity on {self.part.name} by {self.created_by.username if self.created_by else 'Unknown'}"