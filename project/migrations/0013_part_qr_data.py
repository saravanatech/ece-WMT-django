# Generated by Django 4.1.7 on 2024-07-29 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_part_vendor_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='qr_data',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
