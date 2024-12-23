# Generated by Django 3.2.10 on 2024-10-17 03:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('first_operation', '0003_batchlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fo_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='batchitems',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fo_bi_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='batchnestingitems',
            name='nesting_number',
            field=models.CharField(db_index=True, default='N1', max_length=50),
        ),
        migrations.AddField(
            model_name='batchnestingitems',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fo_bni_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='batch',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fo_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='batchitems',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fo_bi_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='batchnestingitems',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fo_bni_created_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
