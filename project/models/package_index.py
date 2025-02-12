from enum import Enum
from project.models.parts import Part
from django.contrib.auth.models import User

from project.models.project import Project
from django.db import models

class PackageIndex(models.Model):
    class Status(Enum):
        Empty = 0
        AllocationDone = 1
        PackingSlipGenerated = 2
        ReceivedInFactory=8
        Loaded = 10
        UnLoaded = 9
    
    part = models.ForeignKey(Part,  on_delete=models.CASCADE, db_index=True, related_name='package_index')
    ProjectNo = models.CharField(max_length=100, blank=True, null=True)
    packageName = models.CharField(max_length=200, blank=False, null=False, db_index=True)
    packAgeIndex = models.IntegerField()
    revision = models.IntegerField(default=1)
    partsSelectedIndex = models.CharField(max_length=255, default='', blank=True, null=True)
    status = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.part.part_description
