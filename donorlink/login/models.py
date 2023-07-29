from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    role = models.CharField(max_length=10)

class Donor(models.Model):
    uuser = models.OneToOneField(User,on_delete=models.CASCADE,related_name='donor')
    phoneno = models.IntegerField()
    age = models.IntegerField()
    bg = models.CharField(max_length=10)
    district = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    document = models.FileField(upload_to='pdfs/donor/')  

class Bloodbank(models.Model):
    uuser = models.OneToOneField(User,on_delete=models.CASCADE,related_name='bloodbank')
    phoneno = models.IntegerField()
    city = models.CharField(max_length=20)
    document = models.FileField(upload_to='pdfs/bloodbank/')

class Hospital(models.Model):
    uuser = models.OneToOneField(User,on_delete=models.CASCADE,related_name='hospital')
    phoneno = models.IntegerField()
    city = models.CharField(max_length=20)
    document = models.FileField(upload_to='pdfs/hospital/')

class Patient(models.Model):
    hosp = models.ForeignKey(Hospital,on_delete=models.CASCADE,related_name='patients')
    pid = models.AutoField(primary_key=True, default=1000,verbose_name='ID')
    name = models.CharField(max_length=25)
    purpose = models.CharField(max_length=20)
    doctor  = models.CharField(max_length=20)
    phoneno = models.IntegerField()
    email = models.EmailField()
    age = models.IntegerField()
    bg = models.CharField(max_length=10)
    district = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    document = models.FileField(upload_to='pdfs/patients/')

class Bankstock(models.Model):
    bank = models.OneToOneField(Bloodbank,on_delete=models.CASCADE,related_name='bankstock')
    ap = models.IntegerField(default=5)
    an = models.IntegerField(default=5)
    bp = models.IntegerField(default=5)
    bn = models.IntegerField(default=5)
    abp = models.IntegerField(default=5)
    abn = models.IntegerField(default=5)
    op = models.IntegerField(default=5)
    on = models.IntegerField(default=5)
