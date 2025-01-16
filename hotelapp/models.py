from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Rooms(models.Model):
    rname=models.CharField(max_length=70,verbose_name="Room Name")
    btype=((1,"Single"),(2,"Double"),(3,"Multiple"))
    bedtypecat=models.IntegerField(verbose_name='Bed Type',choices=btype)
    nbed=models.IntegerField(verbose_name="No. of Bed")
    Price=models.FloatField()
    rdesc=models.CharField(max_length=500,verbose_name="Description")
    rsize=models.FloatField(verbose_name="Size")
    Address=models.CharField(max_length=200)
    Location=models.CharField(max_length=25)
    City=models.CharField(max_length=25)
    cimage=models.ImageField(upload_to='image')
    cphoto1=models.ImageField(upload_to='image')
    cphoto2=models.ImageField(upload_to='image')
    swim=models.BooleanField(default=False,verbose_name="Swimming Pool")
    garden=models.BooleanField(default=False,verbose_name="Garden")

    def __str__(self):
        return self.rname
    
class Roombooking(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    rid=models.ForeignKey(Rooms,on_delete=models.CASCADE,db_column="rid")
    checkin=models.DateTimeField()
    checkout=models.DateTimeField()
    cname=models.CharField(max_length=50,verbose_name="Client")
    mob=models.BigIntegerField(verbose_name="Mobile")
    email=models.EmailField()
    adults=models.IntegerField()
    child=models.IntegerField()
    stat=((1,"Success"),(2,"Booked"),(3,"Canceled"),(4,'pending'))
    status=models.IntegerField(choices=stat)
    
