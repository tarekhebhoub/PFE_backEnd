from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import generics
from django.shortcuts import get_object_or_404
from . import models
from . import serializers
from rest_framework.views import APIView


    
class EmployeeCreate(generics.CreateAPIView):
    authentication_classes=()
    permission_classes=()
    serializer_class=serializers.UserSerializer
    def post(self,request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = models.Employee.objects.create_user(**serializer.validated_data)
            token=Token.objects.create(user=user)
            serializer = serializers.UserSerializer(user)
            data=serializer.data
            data["token"]=user.auth_token.key
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    permission_classes=()
    serializer_class=serializers.LoginSerializer
    def post(self,request):
        username=request.data.get("username")
        password=request.data.get("password")
        print(username)
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
    
    
class StructureView (APIView):
    serializer_class = serializers.StructureSerializer
    permission_classes=()
    authentication_classes=()


    def get(self,request):
        queryset=models.Structure.objects.all()
        serializer=serializers.StructureSerializer(queryset,many=True)
        # data=[]
        # for x in serializer.data:
        #     data.append(x['Nom_struc'])
        # print(data)
        print(serializer.data)
        return Response(serializer.data) 
    
class DepartementView (APIView):
    serializer_class = serializers.DepartementSerializer
    permission_classes=()
    authentication_classes=()    
    def get(self,request,pk):
        structure=models.Structure.objects.get(id=pk)
        departement=models.Departement.objects.filter(id_struc=structure.id)
        serializer=serializers.DepartementSerializer(departement,many=True)
        
        return Response(serializer.data) 
        # return Response(serializer.data)

class OffrelistView (APIView):
    serializer_class = serializers.OffreEmpSerializer

    def get(self,request):
        queryset=models.OffreEMP.objects.all()
        serializer=serializers.OffreEmpSerializer(queryset,many=True)
        # data=[]
        # for x in serializer.data:
        #     data.append(x['Nom_struc'])
        # print(data)
        print(serializer.data)
        return Response(serializer.data) 
    def post(self,request):
        serializer = serializers.OffreEmpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)
    

class OffreView(APIView):
    serializer_class=serializers.OffreEmpSerializer
    def get(self,request,pk):
        offre=get_object_or_404(models.OffreEMP,id=pk)


        serializer=serializers.OffreEmpSerializer(offre)
        data=serializer.data


        print(serializer.data)
        return Response(data,status=status.HTTP_200_OK)
    def delete(self,request,pk):
        if request.user.is_superuser:
            offre=get_object_or_404(models.OffreEMP,id=pk)
            offre.delete()
            return Response("delete succefuly",status=status.HTTP_204_NO_CONTENT)
        return Response({"U are not Admin"},status=status.HTTP_400_BAD_REQUEST)
    def put(self,request,pk):
        if request.user.is_superuser:
            offre=get_object_or_404(models.OffreEMP,id=pk)
            serializer=serializers.OffreEmpSerializer(offre,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({"U are not Admin"},status=status.HTTP_400_BAD_REQUEST)    