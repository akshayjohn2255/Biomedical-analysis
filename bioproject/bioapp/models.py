from django.db import models

# Create your models here.

class admin(models.Model):
    uname=models.CharField(max_length=100)
    pwd=models.CharField(max_length=100)
    mailid=models.EmailField(max_length=100)

class udetails(models.Model):
    uid=models.IntegerField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email=models.EmailField(max_length=100,unique=True)
    uname=models.CharField(max_length=100,unique=True)
    pwd=models.CharField(max_length=100)
    ph=models.CharField(max_length=100)
    dob = models.DateField()

class dProfile(models.Model):
    did=models.IntegerField(primary_key=True)
    lno = models.CharField(max_length=100,unique=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField(max_length=100,unique=True)
    ph = models.CharField(max_length=100)
    qual= models.CharField(max_length=100)
    spec=  models.CharField(max_length=150)
    exp= models.DateField()
    uname=models.CharField(max_length=100,unique=True)
    pwd = models.CharField(max_length=100)
    file=models.CharField(max_length=100)
    status = models.CharField(max_length=40)


class contents(models.Model):
    did=models.ForeignKey(dProfile,on_delete=models.CASCADE)
    keyword=models.CharField(max_length=100)
    url=models.URLField(max_length=254,unique=True)
    rank=models.IntegerField(default=-1)
    status=models.CharField(max_length=100)


