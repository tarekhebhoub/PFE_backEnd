from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

import hashlib

from .models import User,Pos_User
from .serializers import UserSerializer,LoginSerializer,PositionSerializer

class UserCreate(generics.CreateAPIView):
    authentication_classes=()
    permission_classes=()
    serializer_class=UserSerializer
    def post(self,request):
        try:
            user=User(
                email=request.data.get('email'),
                username=request.data.get('username'),
                first_name=request.data.get('first_name'),
                last_name=request.data.get('last_name'),
                matricule=request.data.get('matricule'),
                num_phone=request.data.get('num_phone')
            )
            user.set_password(request.data.get('password'))
            user.save()
            token=Token.objects.create(user=user)
            return Response({"token":user.auth_token.key,"username":user.username})
        except:
            return Response({"error":"the username already exist"})
class LoginView(APIView):
    permission_classes=()
    serializer_class=LoginSerializer
    def post(self,request):
        username=request.data.get("username")
        password=request.data.get("password")

        user=authenticate(username=username,password=password)
        if user:
            Token.objects.create(user=user)
            return Response({"token":user.auth_token.key,"username":user.username},status=status.HTTP_200_OK)
        else:
            return Response({"error":"Wrong Credentials"},status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return Response({"Logout successfully"},status=status.HTTP_200_OK)



class Lock(APIView):
   
    def crypt_lock(self,matricule):
        # plaintext = matricule
        # key = Fernet.generate_key()
        # plaintext_bytes = plaintext.encode()
        # cipher = Fernet(key)
        # encrypted_bytes = cipher.encrypt(plaintext_bytes)
        # encrypted_string = encrypted_bytes.decode()
        # return encrypted_string


        message = matricule
        hash_object = hashlib.sha256(message.encode())
        hash_hex = hash_object.hexdigest()
        return hash_hex
        
    def get(self,request):
        lock=self.crypt_lock(request.user.matricule)
        return Response({"lock":lock})


class Position(APIView):
    serializer_class=PositionSerializer
    def get(self,request):
        pos_user=Pos_User.objects.get(user=request.user.id)
        serializer=PositionSerializer(pos_user)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        # data=JSONParser().parse(request.data)
        data={'user':request.user.id}
        data.update(request.data)
        serializer=PositionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def put(self,request):
        pos_user=Pos_User.objects.get(user=request.user.id)
        pos_user.latitude=request.data.get("latitude")
        pos_user.longitude=request.data.get("longitude")
        
        pos_user.save()
        serializer=PositionSerializer(pos_user)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
        

@api_view(('GET',))
def get_pos(request):
    pos_users=Pos_User.objects.all()
    serializer=PositionSerializer(pos_users,many=True)
    return Response(serializer.data)