# Generated by Django 4.1.7 on 2024-09-06 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0035_remove_part_vehicle_part_vehicle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='part',
            name='vehicle',
        ),
        migrations.AddField(
            model_name='part',
            name='vehicle',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='project.vehicle'),
        ),
    ]