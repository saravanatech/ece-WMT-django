from django.db import models

from project.models.parts import Part
from django.contrib.auth.models import User

from project.models.project import Project

class PartLog(models.Model):
    part = models.ForeignKey(Part,  on_delete=models.CASCADE, db_index=True, related_name='part_logs')
    project = models.ForeignKey(Project,  on_delete=models.CASCADE, db_index=True, null=True, blank=True)
    logMessage = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=50, default='info', blank=True, null=True)
    created_by = models.ForeignKey(User,  on_delete=models.SET_NULL, db_index=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.part.part_description
