# Generated by Django 3.0.5 on 2023-06-03 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_auto_20230603_1427'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='id',
            new_name='pid',
        ),
    ]