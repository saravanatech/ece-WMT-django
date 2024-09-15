from django.db import models

class Ebom(models.Model):
    customer_name = models.CharField(max_length=255, db_index=True, null=False, blank=False)
    group_code = models.CharField(max_length=50, db_index=True, null=False, blank=False)
    part_description = models.CharField(max_length=255)
    part_number = models.CharField(max_length=100)
    product_type = models.CharField(max_length=100)
    project_name = models.CharField(max_length=255, db_index=True, null=False, blank=False)
    project_no = models.CharField(max_length=100, db_index=True, null=False, blank=False)
    qty = models.IntegerField()
    uom = models.CharField(max_length=50)
    po_mo_no = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, default='')
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_no
