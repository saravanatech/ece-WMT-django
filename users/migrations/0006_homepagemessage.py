# Generated by Django 4.1.4 on 2023-07-31 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_userprofile_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=500)),
                ('created_by', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
