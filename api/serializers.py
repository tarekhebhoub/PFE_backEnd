from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import User,Pos_User,Station
from django.contrib.auth import authenticate
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('first_name','last_name','username','email','password','sold')
        extra_kwargs={'password':{'write_only':True}}

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
