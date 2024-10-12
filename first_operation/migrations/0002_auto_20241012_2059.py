# Generated by Django 3.2.10 on 2024-10-12 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('first_operation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_no', models.CharField(db_index=True, max_length=100)),
                ('date', models.DateField(db_index=True, max_length=50, null=True)),
                ('status', models.IntegerField(db_index=True, default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BatchItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(db_index=True, default=0)),
                ('rm_code', models.CharField(db_index=True, max_length=100)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('thickness', models.DecimalField(decimal_places=1, default=0, max_digits=5)),
                ('item_code', models.CharField(db_index=True, max_length=100)),
                ('qty', models.IntegerField(default=0)),
                ('nesting_no', models.CharField(max_length=50)),
                ('sheet_thickness', models.DecimalField(decimal_places=1, default=0, max_digits=5)),
                ('material', models.CharField(db_index=True, max_length=255)),
                ('nesting_count', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('error', models.BooleanField(default=False)),
                ('error_message', models.CharField(db_index=True, max_length=255)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first_operation.batch')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='rmcodemaster',
            name='sheet_thickness',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5),
        ),
        migrations.CreateModel(
            name='BatchNestingItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nesting_item_code', models.CharField(db_index=True, max_length=100)),
                ('item_qty', models.IntegerField(default=1)),
                ('status', models.IntegerField(default=0)),
                ('batch_items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first_operation.batchitems')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
