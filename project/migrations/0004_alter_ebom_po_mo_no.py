# Generated by Django 4.1.7 on 2024-07-22 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_alter_ebom_customer_name_alter_ebom_group_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebom',
            name='po_mo_no',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
