# Generated by Django 4.1.7 on 2024-07-22 03:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebom',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ebom',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='ebom',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
