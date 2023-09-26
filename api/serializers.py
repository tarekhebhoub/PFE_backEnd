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
    # Id_dep = serializers.SlugRelatedField(
    #     slug_field='Nom_dep',
    #     queryset=models.Departement.objects.all()
    # )
    # Id_struc = serializers.SlugRelatedField(
    #     slug_field='Nom_struc',
    #     queryset=models.Structure.objects.all()
    # )
    class Meta:
        model=models.Employee
        fields=('id','first_name','last_name','email','is_stricture','is_commission','is_superuser','is_departement')

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



class OffrePostEmpSerializer(serializers.ModelSerializer):

    class Meta:
        model= models.OffreEMP
        fields='__all__'   

class FichierSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.FichierBourse
        fields='__all__'

class FichierSerializer2(serializers.ModelSerializer):
    class Meta:
        model= models.ParcoursProf
        fields='__all__'        

class ResumeSerializer(serializers.ModelSerializer):
    Id_dep = serializers.SlugRelatedField(
        slug_field='Nom_dep',
        queryset=models.Departement.objects.all()
    )
    Id_struc = serializers.SlugRelatedField(
        slug_field='Nom_struc',
        queryset=models.Structure.objects.all()
    )
    class Meta:
        model= models.Employee
        fields=['first_name','last_name','email','Photo','Date_Naiss','Adresse_perso','Date_Recrut','Poste_actuel','Telephone','Id_dep','Id_struc','Echelle']  

class DepartementsSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Employee
        fields=['username','password','Id_struc','Id_dep']


class EmployeeNameSerializerField(serializers.Field):
    def to_representation(self, value):
        return f"{value.first_name} {value.last_name}"


class DepFichierSerializer(serializers.ModelSerializer):
    # id_Emp = EmployeeNameSerializerField( read_only=True)
    class Meta:
        model=models.FichierBourse
        fields='__all__'



class FileSerializerForDep(serializers.ModelSerializer):
    class Meta:
        model=models.FichierBourse
        fields=['NomRespo','PrenomRespo','response_Dep','fanction','CompetanceRespo','Commentaire']


