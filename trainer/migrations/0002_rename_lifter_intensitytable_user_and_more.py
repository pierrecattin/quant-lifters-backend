# Generated by Django 5.0.1 on 2024-02-19 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='intensitytable',
            old_name='lifter',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='workout',
            old_name='lifter',
            new_name='user',
        ),
    ]
