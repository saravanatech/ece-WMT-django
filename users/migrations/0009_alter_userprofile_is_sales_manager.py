# Generated by Django 4.1.4 on 2023-08-15 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_userprofile_is_sales_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='is_sales_manager',
            field=models.BooleanField(default=False, help_text='Note: If this is enabled, is Sales will be enabled automatically'),
        ),
    ]
