# Generated by Django 4.1.7 on 2024-07-31 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0021_alter_part_part_package_mapping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='part_package_mapping',
            field=models.TextField(blank=True, default='', max_length=800, null=True),
        ),
    ]
