from django.db import models

# Create your models here.
class appointment(models.Model):
    appointid = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    name = models.CharField(max_length=30)
    age = models.CharField(max_length=10)
    email = models.CharField(max_length=25)
    address = models.CharField(max_length=250)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=15)
    result = models.CharField(max_length=30)
    blood_group = models.CharField(max_length=12, default='')

class posative(models.Model):
    posativid = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    name = models.CharField(max_length=30)
    age = models.CharField(max_length=10)
    email = models.CharField(max_length=25)
    address = models.CharField(max_length=100)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=15)
    result = models.CharField(max_length=30)
    appoint =models.ForeignKey(appointment,on_delete=models.CASCADE, related_name='posative')
    
class neagtive(models.Model):
    negativeid = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    name = models.CharField(max_length=30)
    age = models.CharField(max_length=10)
    email = models.CharField(max_length=25)
    address = models.CharField(max_length=100)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=15)
    result = models.CharField(max_length=30)
    appoint =models.ForeignKey(appointment,on_delete=models.CASCADE)
   
class donor(models.Model):
    donorid = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    name = models.CharField(max_length=30)
    age = models.CharField(max_length=10)
    email = models.CharField(max_length=25)
    address = models.CharField(max_length=100)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=15)
    result = models.CharField(max_length=30) 
    blood_group = models.CharField(max_length=12, default='')
       