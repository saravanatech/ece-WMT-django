# Generated by Django 3.2.10 on 2025-03-17 17:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0044_auto_20250317_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendorrejectionhistory',
            name='assigned_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2025, 3, 17, 17, 31, 16, 473803, tzinfo=utc), null=True),
        ),
    ]
