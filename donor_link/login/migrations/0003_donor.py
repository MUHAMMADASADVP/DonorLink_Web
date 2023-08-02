# Generated by Django 3.0.5 on 2023-05-25 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneno', models.IntegerField()),
                ('age', models.IntegerField()),
                ('bg', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=20)),
                ('document', models.FileField(upload_to='pdfs/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='donor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]