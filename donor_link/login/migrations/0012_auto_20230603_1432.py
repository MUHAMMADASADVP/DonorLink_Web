# Generated by Django 3.0.5 on 2023-06-03 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_auto_20230603_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='pid',
            field=models.AutoField(default=1000, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]