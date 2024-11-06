# Generated by Django 3.2.10 on 2024-10-20 17:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('first_operation', '0006_auto_20241020_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fo_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='batch',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fo_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]