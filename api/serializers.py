from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import User,Pos_User,Station,Card,Transaction,Reservation,Location,Velo
from django.contrib.auth import authenticate
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('first_name','last_name','username','email','password','matricule','sold','gender')
        extra_kwargs={'password':{'write_only':True}}
class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

    # def create(self,validated_data):
    #     user=User(
    #         email=validated_data['email'],
    #         username=validated_data['username'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name'],
    #         matricule=validated_data['matricule'],
    #         num_phone=validated_data['num_phone']
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     token=Token.objects.create(user=user)
    #     return Response({"token":"tarek"})

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username','password')

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Pos_User
        fields='__all__'

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Station
        fields='__all__'

class VelosSerializer(serializers.ModelSerializer):
    class Meta:
        model=Velo
        fields='__all__'

class CardSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=100,required=False)
    class Meta:
        model=Card
        fields=['id','balance','token']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields='__all__'

class LocationSerializer(serializers.ModelSerializer):
    date_close=serializers.DateTimeField(required=False)
    class Meta:
        model=Location
        fields='__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reservation
        fields='__all__'