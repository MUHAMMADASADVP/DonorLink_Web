# Generated by Django 3.0.5 on 2023-06-19 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0016_auto_20230614_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodbank',
            name='district',
            field=models.CharField(default='kannur', max_length=10),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Donationlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('dbank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.Bloodbank')),
                ('ddonor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.Donor')),
            ],
        ),
    ]
