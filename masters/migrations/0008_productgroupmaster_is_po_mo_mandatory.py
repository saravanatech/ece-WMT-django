# Generated by Django 4.1.7 on 2024-08-04 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0007_productgroupmaster_qr_code_scanning_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productgroupmaster',
            name='is_po_mo_mandatory',
            field=models.BooleanField(default=False),
        ),
    ]
