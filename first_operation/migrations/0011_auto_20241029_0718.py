# Generated by Django 3.2.10 on 2024-10-29 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_operation', '0010_alter_batchitems_batch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batchitems',
            name='sheet_thickness',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='rmcodemaster',
            name='sheet_thickness',
            field=models.CharField(max_length=10),
        ),
    ]
