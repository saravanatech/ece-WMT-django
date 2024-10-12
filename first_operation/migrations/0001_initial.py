# Generated by Django 3.2.10 on 2024-10-12 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemTypeMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_no', models.IntegerField(default=0)),
                ('item_code', models.CharField(db_index=True, max_length=100, unique=True)),
                ('type', models.CharField(max_length=50, null=True)),
                ('status', models.BooleanField(db_index=True, default='False')),
            ],
        ),
        migrations.CreateModel(
            name='RMCodeMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_no', models.IntegerField(default=0)),
                ('rm_code', models.CharField(db_index=True, max_length=100)),
                ('description', models.CharField(max_length=255, null=True)),
                ('sheet_thickness', models.IntegerField(db_index=True, default=0)),
                ('material', models.CharField(max_length=255)),
                ('status', models.BooleanField(db_index=True, default='False')),
            ],
            options={
                'unique_together': {('rm_code', 'sheet_thickness')},
            },
        ),
    ]