from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class User(AbstractUser):
    sold=models.IntegerField(default=10)
    matricule=models.CharField(max_length=15,primary_key=True)
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
    def __str__(self):
        return self.state+' '+str(self.id)
    

class Alocation_Velo(models.Model):
    velo=models.ForeignKey(Velo,on_delete=models.CASCADE,related_name="velo_located")
    user=models.ForeignKey(User,related_name="user_of_velo",on_delete=models.CASCADE) 
    date_open=models.DateTimeField()
    date_close=models.DateTimeField()

# class Voucher(models.Model):
#  (Id , string ,value, user, uses, validity)

def generate_token():
    return str(uuid.uuid4())

class Card(models.Model):
    token = models.CharField(max_length=100, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    used = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = generate_token()
        super(Card, self).save(*args, **kwargs)


# class Transaction(models.Model):
#     card = models.ForeignKey(Card, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)