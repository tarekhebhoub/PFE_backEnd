from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
from django.db.models import Q

import pytz
import datetime
import hashlib

from .models import User,Pos_User,Station,Card,Velo,Reservation,Location
from .serializers import (UserSerializer,LoginSerializer,
                        PositionSerializer,StationSerializer,CardSerializer,
                        TransactionSerializer,LocationSerializer,ReservationSerializer)

class UserCreate(generics.CreateAPIView):
    authentication_classes=()
    permission_classes=()
    serializer_class=UserSerializer
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)
            token=Token.objects.create(user=user)
            serializer = UserSerializer(user)
            data=serializer.data
            data["token"]=user.auth_token.key
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)
        # try:
    #     user=User(request.data)
    # #     email=request.data.get('email'),
    # #     username=request.data.get('username'),
    # #     first_name=request.data.get('first_name'),
    # #     last_name=request.data.get('last_name'),
    # # )
    # # user.set_password(request.data.get('password'))
   
    #     user.save()
    #     token=Token.objects.create(user=user)
    #     return Response({"token":user.auth_token.key,"username":user.username},status=status.HTTP_201_CREATED)
        # except:
        #     return Response("username already exists",status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes=()
    serializer_class=LoginSerializer
    def post(self,request):
        username=request.data.get("username")
        password=request.data.get("password")

        user=authenticate(username=username,password=password)
        if user:
            try:
                Token.objects.create(user=user)
                serializer = UserSerializer(user)
                data=serializer.data
                data["token"]=user.auth_token.key
                return Response(data)
                #return Response({"token":user.auth_token.key,"username":user.username})
            except:
                return Response({'token already exists'})
        else:
            return Response({"error":"Wrong Credentials"},status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
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
    
class StationsView(APIView):
    serializer_class=StationSerializer
    def get(self,request):
        station = Station.objects.all()
        serializer=StationSerializer(station,many=True)
        data=serializer.data
        for x in data:
            print("_________________________")
            id=x["id"]
            station=Station.objects.get(id=id)
            x["stock"]=len(station.velos.all())
            print(x["stock"])
        #print(serializer.data)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        if request.user.is_superuser:
            serializer=StationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({"U are not Admin"},status=status.HTTP_400_BAD_REQUEST)
    


class StationView(APIView):
    serializer_class=StationSerializer
    def get(self,request,pk):
        station=get_object_or_404(Station,id=pk)

        # station = Station.objects.get(id=pk)
        serializer=StationSerializer(station)
        data=serializer.data
        data["stock"]=len(station.velos.all())
        
        print(serializer.data)
        return Response(data,status=status.HTTP_200_OK)
    def delete(self,request,pk):
        if request.user.is_superuser:
            station=get_object_or_404(Station,id=pk)
            station.delete()
            return Response("delete succefuly",status=status.HTTP_204_NO_CONTENT)
        return Response({"U are not Admin"},status=status.HTTP_400_BAD_REQUEST)
    def put(self,request,pk):
        if request.user.is_superuser:
            station=get_object_or_404(Station,id=pk)
            serializer=StationSerializer(station,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({"U are not Admin"},status=status.HTTP_400_BAD_REQUEST)


@api_view(('GET',))
def get_pos(request):
    if request.user.is_superuser:
        print(request.headers.get('Authorization'))
        pos_users=Pos_User.objects.all()
        serializer=PositionSerializer(pos_users,many=True)
        return Response(serializer.data)
    return Response({"u are not admin"})

class ReservationView(APIView):
    serializer_class=ReservationSerializer
    def post(self,request):
        station=request.data.get("station")
        velos=Velo.objects.filter(Q(station=station)&Q(state=False))
        # velo=get_object_or_404(Velo,station=station,state=False)
        try:
            velo=velos[0]
        except:
            return Response({"no velo disponible"})
        data={"user":request.user.id,"velo":velo.id,"station":velo.station}
        serializer=ReservationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            velo.station=None
            velo.state=True
            velo.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        # import datetime
        # current_time = datetime.datetime.now()
        # print("The current time is:", current_time)
        # serializer=ReservationSerializer(data=request.data)
        # if serializer.is_valid():
        #     station=request.data.get('station')
        #     velo=get_object_or_404(Velo,station=station,state=False)
        #     velo.station=None
        #     velo.state=True
        #     velo.save()
        #     serializer.save()
        #     return Response(serializer.data,status=status.HTTP_200_OK)
        # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request):
        reservation=Reservation.objects.get(user=request.user.id)
        velo=Velo.objects.get(id=reservation.velo.id)
        velo.state=False
        station=station=request.data.get("station")
        station=Station.objects.get(id=station)
        velo.station=station
        velo.save()
        reservation.delete()
        return Response({"done!"},status=status.HTTP_200_OK)
class LocationView(APIView):
    serializer_class=LocationSerializer
    def post(self,request):
        current_time = datetime.datetime.now()
        reservation=Reservation.objects.get(user=request.user.id)
        data={"date_open":current_time,"reservation":reservation.id}
        serializer=LocationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request):
        tz = pytz.timezone('Etc/GMT')
        current_time=datetime.datetime.now()
        current_time = tz.localize(current_time)
        print(current_time)
        reservation=get_object_or_404(Reservation,user=request.user.id)
        location=get_object_or_404(Location,reservation=reservation.id)
        try: 
            station=request.data.get("station")
        except:
            return Response({"please select the station"})
        station=get_object_or_404(Station,id=station)
        date_open=location.date_open
        print(date_open)
        velo=Velo.objects.get(id=reservation.velo.id)
        if station:
            sold=int(int((current_time - date_open).total_seconds())/60)*20
            user=User.objects.get(id=request.user.id)
            user.sold-=sold
            sold=user.sold
            user.save()
            location.delete()
            reservation.delete()
            #serializer=LocationSerializer(location,data=data)
            # if serializer.is_valid():
            #     velo.station=station
            #     velo.state=False
            #     velo.save()
            #     reservation.delete()
            #     serializer.save()
            #     return Response(serializer.data,status=status.HTTP_200_OK)
            # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response({"sold: ":sold},status=status.HTTP_200_OK)
        return Response({"enter the station"})

class CardView(APIView):
    serializer_class=CardSerializer
    def get(sekf,request):
        if request.user.is_superuser:
            cards=Card.objects.all()
            serializer=CardSerializer(cards,many=True)
            
            return Response(serializer.data)
        return Response({"U are not Admin"})
    def post(self,request):
        if request.user.is_superuser:
            serializer=CardSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({"U are not Admin"},status=status.HTTP_400_BAD_REQUEST)

class CardViewPk(APIView):
    def get(self,request,pk):
        if request.user.is_superuser:
            card=get_object_or_404(Card,id=pk)
            serializer=CardSerializer(card)
            return Response(serializer.data)
        return Response({"u r not an admin"})
        def delete(self,request,pk):
            if request.user.is_superuser:
                card=get_object_or_404(Card,id=pk)
                card.delete()
                return Response("delete succefuly",status=status.HTTP_204_NO_CONTENT)
            return Response({"U are not Admin"},status=status.HTTP_400_BAD_REQUEST)
        def put(self,request,pk):
            if request.user.is_superuser:
                card=get_object_or_404(Card,id=pk)
                serializer=CardSerializer(card,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response({"U are not Admin"},status=status.HTTP_400_BAD_REQUEST)

class SoldView(APIView):
    serializer_class=TransactionSerializer
    def post(self, request):
        token = request.data.get('token')
        card = get_object_or_404(Card, token=token, used=False)
        user=get_object_or_404(User,id=request.user.id)
        data={"card":card.id,"user":user.id}
        serializer=TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user.sold+=card.balance
            card.used=True
            card.save()
            user.save()
            return Response({"sold":user.sold})
        print("____________________________")
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



