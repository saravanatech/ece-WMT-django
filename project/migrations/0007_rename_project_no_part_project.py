# Generated by Django 4.1.7 on 2024-07-22 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_part'),
    ]

    operations = [
        migrations.RenameField(
            model_name='part',
            old_name='project_no',
            new_name='project',
        ),
    ]