# Generated by Django 3.2.10 on 2024-10-20 16:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('first_operation', '0005_alter_batchlog_batch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batchitems',
            name='nesting_no',
        ),
        migrations.AlterField(
            model_name='batchitems',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fo_bi_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='batchitems',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fo_bi_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='batchnestingitems',
            name='batch_items',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batch_items', to='first_operation.batchitems'),
        ),
    ]