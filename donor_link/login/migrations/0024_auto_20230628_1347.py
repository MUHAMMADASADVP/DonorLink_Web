# Generated by Django 3.0.5 on 2023-06-28 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0023_auto_20230628_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='certificate',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
