# Generated by Django 4.1.7 on 2024-08-02 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0023_part_qr_code_scanning_part_use_qr_code_scanning'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='scanned_packages',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
