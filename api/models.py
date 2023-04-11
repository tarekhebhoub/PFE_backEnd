from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    sold=models.IntegerField(default=10)
    def __str__(self):
        return self.username

class Pos_User(models.Model):
    user=models.OneToOneField(User,related_name="pos_of_user",on_delete=models.CASCADE)
    latitude=models.FloatField(default=0)
    longitude=models.FloatField(default=0)
    def __str__(self):
        return "position: "+ str(self.user)


class Station(models.Model):
    name=models.CharField(max_length=50)
    latitude=models.FloatField()
    longitude=models.FloatField()
    def __str__(self):
        return self.name

class Velo(models.Model):
    # lock=models.CharField(max_length=50)    
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='velos')
    state=models.CharField(max_length=15)
    latitude=models.FloatField()
    longitude=models.FloatField()
    # date_open=models.DateTimeField()
    # date_close=models.DateTimeField()

    
