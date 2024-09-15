from django.db import models
from django import forms

from masters.models.vendor import VendorMasters

class ProductGroupMaster(models.Model):
    s_no = models.IntegerField(default=0)
    product = models.CharField(max_length=100, db_index=True)
    group_code = models.CharField(max_length=100, db_index=True)     
    description = models.CharField(max_length=255, blank=False, null=True) 
    packing_name = models.CharField(max_length=255, db_index=True)
    fixed = models.CharField(max_length=10, db_index=True) 
    no_of_packages = models.CharField(max_length=150)
    status = models.BooleanField(default='False', db_index=True)
    wh_team_name = models.CharField(max_length=255, db_index=True)
    source_of_supply = models.CharField(max_length=255, db_index=True)
    vendors = models.ManyToManyField(VendorMasters, blank=True,  related_name='vendors')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    qr_type = models.CharField(max_length=50, db_index=True, default='Type-1')
    use_qr_code_scanning = models.BooleanField(default=False)
    qr_code_scanning=models.CharField(max_length=100, db_index=True, null=True, blank=True)
    is_po_mo_mandatory = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('product', 'group_code')

    def __str__(self):  # __unicode__ on Python 2
        return str(self.group_code)
    


class ProductGroupMasterUploadForm(forms.Form):
    file = forms.FileField()