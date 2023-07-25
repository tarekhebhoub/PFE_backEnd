from rest_framework import serializers
from . import models
from django.contrib.auth import authenticate
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Employee
        fields=('first_name','last_name','username','email','password','Date_Naiss','Adresse_perso','Date_Recrut','Poste_actuel','Telephone','Id_dep','Photo')
        extra_kwargs={'password':{'write_only':True}}


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Employee
        fields=('username','password')



class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Employee
        fields='__all__'

class StructureSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.Structure
        fields='__all__'

class DepartementSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.Departement
        fields='__all__'

class OffreEmpSerializer(serializers.ModelSerializer):
    Id_dep = serializers.SlugRelatedField(
        slug_field='Nom_dep',
        queryset=models.Departement.objects.all()
    )
    Id_struc = serializers.SlugRelatedField(
        slug_field='Nom_struc',
        queryset=models.Structure.objects.all()
    )
    
    class Meta:
        model= models.OffreEMP
        fields='__all__'        

class FichierSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.OffreEMP
        fields='__all__'