# Generated by Django 4.1.7 on 2024-07-29 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_part_qr_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='vendor_status',
            field=models.IntegerField(default=0),
        ),
    ]