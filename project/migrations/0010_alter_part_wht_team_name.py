# Generated by Django 4.1.7 on 2024-07-23 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_part_bay_in_part_bay_out_part_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='wht_team_name',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
