# Generated by Django 4.1.7 on 2024-07-30 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0015_remove_partlog_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partlog',
            name='type',
            field=models.CharField(blank=True, default='info', max_length=50, null=True),
        ),
    ]
