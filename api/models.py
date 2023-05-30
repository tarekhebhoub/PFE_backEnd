from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class User(AbstractUser):
    sold=models.IntegerField(default=100)
    matricule=models.CharField(max_length=15,unique=True,null=True)
    usage=models.IntegerField(default=0)
    gender=models.BooleanField()
    active=models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username

class Pos_User(models.Model):
    user=models.OneToOneField(User,related_name="pos_of_user",on_delete=models.CASCADE)
    latitude=models.FloatField()
    longitude=models.FloatField()
    velo=models.OneToOneField('Velo',related_name="pos_of_user_velo",on_delete=models.CASCADE)
    def __str__(self):
        return "position: "+ str(self.user)


class Station(models.Model):
    name=models.CharField(max_length=50,unique=True)
    latitude=models.FloatField()
    longitude=models.FloatField()
    def __str__(self):
        return self.name

class Velo(models.Model):
    # lock=models.CharField(max_length=50)
    name=models.CharField(max_length=50,unique=True)
    code=models.IntegerField(null=False,blank=False)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='velos',null=True,blank=True)
    state=models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)+' '+ str(self.state)

class Reservation(models.Model):
    velo=models.OneToOneField(Velo,on_delete=models.CASCADE,related_name="velo_located")
    user=models.OneToOneField(User,related_name="user_of_velo",on_delete=models.CASCADE)
    velo_name=models.CharField(max_length=50)
    velo_code=models.IntegerField(null=False,blank=False)
    def __str__(self):
        return str(self.velo)+' '+str(self.user)

class Location(models.Model):
    date_open=models.DateTimeField()
    #date_close=models.DateTimeField(null=True)
    reservation=models.ForeignKey(Reservation,on_delete=models.CASCADE,blank=True,related_name="reservation_alocate")
    def __str__(self):
        return str(self.reservation)+' '+str(self.date_open)

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
    def __str__(self):
        return str(self.balance)+' '+ str(self.used)



class Transaction(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)