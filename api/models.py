from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    matricule = models.CharField(max_length=25)
     # = models.ImageField(blank=True)
    num_phone=models.CharField(max_length=25)

    
    def __str__(self):
        return self.username

class Pos_User(models.Model):
    user=models.OneToOneField(User,related_name="pos_of_user",on_delete=models.CASCADE)
    latitude=models.FloatField(default=0)
    longitude=models.FloatField(default=0)
    def __str__(self):
        return "position: "+ str(self.user)

class Velo(models.Model):
    # lock=models.CharField(max_length=50)    
    state=models.CharField(max_length=15)
    latitude=models.FloatField()
    longitude=models.FloatField()
    # date_open=models.DateTimeField()
    # date_close=models.DateTimeField()

    
