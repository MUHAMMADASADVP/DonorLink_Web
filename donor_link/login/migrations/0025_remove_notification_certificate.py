# Generated by Django 3.0.5 on 2023-06-28 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0024_auto_20230628_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='certificate',
        ),
    ]
