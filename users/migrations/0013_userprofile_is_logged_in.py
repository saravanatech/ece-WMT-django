# Generated by Django 4.1.4 on 2024-06-06 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_useractivity'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_logged_in',
            field=models.BooleanField(default=False),
        ),
    ]
