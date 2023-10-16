from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import generics
from django.shortcuts import get_object_or_404
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from .EmailSend import send_email
    
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
        user=authenticate(username=username,password=password)
        if user:
            # refresh = RefreshToken.for_user(user)
            try:
                Token.objects.create(user=user)
            except:
                Token.objects.filter(user=user).delete()
                Token.objects.create(user=user)
                
            return Response({
                "token":str(user.auth_token.key),
                "username":user.username,
                'is_superuser':user.is_superuser,
                'is_departement':user.is_departement,
                'is_stricture':user.is_stricture,
                'is_commission':user.is_commission
                },status=status.HTTP_200_OK)
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
        data=[]
        return Response(serializer.data) 
    def post(self,request):
        serializer = serializers.OffrePostEmpSerializer(data=request.data)
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
    
class FichierListView (APIView):
    serializer_class = serializers.FichierSerializer
    def post(self,request):
        data=request.data
        user_id = Token.objects.get(key=request.auth.key).user_id   
        data['id_Emp']=user_id
        print('tarek')
        serializer=serializers.FichierSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
    def get(self,request):
        queryset=models.FichierBourse.objects.all()
        # search_param = self.request.query_params.get('search', None)
        # if search_param:
        #     queryset = queryset.filter(Nom_personne__icontains=search_param)
        serializer=serializers.FichierSerializer(queryset,many=True)
        for data in serializer.data:
            emp=models.Employee.objects.get(id=data['id_Emp'])
            nom=emp.first_name+' '+emp.last_name
            data['nom']=nom
        # print(search_param)
        return Response(serializer.data) 
    
class FichierView (APIView):

    def delete(self,request,pk1):
        try:
            fichier=models.FichierBourse.objects.get(id=pk1)
        except:
           return Response({"Le fichier n'existe pas"},status=status.HTTP_400_BAD_REQUEST)
        fichier.delete()
        return Response({"Fichier supprimer"},status=status.HTTP_204_NO_CONTENT)
    def put(self,request,pk1):
        id_Emp=request.user.id

        try:
            fichier=models.FichierBourse.objects.get(id=pk1)
        except:
           return Response({"Le fichier n'existe pas"},status=status.HTTP_400_BAD_REQUEST)  
        data=request.data
        data['id_Emp']=id_Emp   
        serializer=serializers.FichierSerializer(fichier,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  
    def get(self,request,pk1):
        try:
            fichier=models.FichierBourse.objects.get(id=pk1)
        except:
            return Response({"Le fichier n'existe pas"},status=status.HTTP_400_BAD_REQUEST)
        
        serializer=serializers.FichierSerializer(fichier)
        return Response(serializer.data)    
    


class Table (APIView):

    def delete(self,request,pk1):
        try:
            fichier=models.ParcoursProf.objects.get(id=pk1)
        except:
           return Response({"Le fichier n'existe pas"},status=status.HTTP_400_BAD_REQUEST)
        fichier.delete()
        return Response({"Fichier supprimer"},status=status.HTTP_204_NO_CONTENT)
    def put(self,request,pk1):
        id_Emp=request.user.id
        try:
            fichier=models.ParcoursProf.objects.get(id=pk1)
        except:
           return Response({"Le fichier n'existe pas"},status=status.HTTP_400_BAD_REQUEST)  
        data=request.data
        data['id_Emp']=id_Emp   
        serializer=serializers.FichierSerializer2(fichier,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  
    def get(self,request,pk1):
        try:
            fichier=models.ParcoursProf.objects.get(id=pk1)
        except:
            return Response({"Le fichier n'existe pas"},status=status.HTTP_400_BAD_REQUEST)
        
        serializer=serializers.FichierSerializer2(fichier)
        return Response(serializer.data) 

class TableListe (APIView):
    serializer_class = serializers.FichierSerializer2
    def post(self,request):
        data=request.data
        user_id = request.user.id
        data['id_Emp']=user_id
        serializer=serializers.FichierSerializer2(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
    def get(self,request):
        queryset=models.ParcoursProf.objects.filter(id_Emp=request.user.id)
        # search_param = self.request.query_params.get('search', None)
        # if search_param:
        #     queryset = queryset.filter(Nom_personne__icontains=search_param)
        serializer=serializers.FichierSerializer2(queryset,many=True)
        # print(search_param)
        return Response(serializer.data)         

class Departements(APIView):
    serializer_class = serializers.DepartementsSerializer
    def post(self,request):
        if request.user.is_superuser:
            data=request.data
            serializer=serializers.DepartementsSerializer(data=data)
            if serializer.is_valid():
                departement= models.Employee.objects.create_user(**serializer.validated_data)
                departement.is_departement=True
                departement.save()
                serializer=serializers.DepartementsSerializer(departement)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
        return Response({"u r not super user"})
    def get(self,request):
        if request.user.is_superuser:
            queryset=models.Employee.objects.filter(is_departement=True)
            serializer=serializers.DepartementsSerializer(queryset,many=True)
            return Response(serializer.data)       
        return Response({"u r not super user"})

#dowload pdf file
@api_view(['GET'])  # Use the appropriate HTTP method for your API
# @permission_classes([IsAuthenticated]) 
def getExigence(request,pk):
        offre=get_object_or_404(models.OffreEMP,id=pk)
        file_to_download = offre.Description
        response = HttpResponse(file_to_download,  content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="contrat"'
        return response
        
# Resume of Profile
@api_view(['GET'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated]) 
def Resume(request):
    user = request.user
    serializer=serializers.ResumeSerializer(user)
    return Response(serializer.data) 


@api_view(['GET'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated]) 
def resumePK(request,pk):
    user=models.Employee.objects.get(id=pk)
    serializer=serializers.ResumeSerializer(user)
    return Response(serializer.data)
# submit of File
@api_view(['PUT'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated]) 
def fileSubmit(request,pk):
    try:
        fichier=models.FichierBourse.objects.get(id=pk)
    except:
        return Response({"Le fichier n'existe pas"},status=status.HTTP_400_BAD_REQUEST)
    fichier.submit_fichier=True
    fichier.save()
    return Response({"done"})

@api_view(['GET'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated]) 
def FileForDep(request):
    requesting_employee=request.user
    print(requesting_employee)
    department = requesting_employee.Id_dep
    employees_in_same_department = models.Employee.objects.filter(Q(Id_dep=department)&Q(is_departement=False))
    employee_ids_in_same_department = employees_in_same_department.values_list('id', flat=True)
    print(employee_ids_in_same_department)

    files_in_same_department = models.FichierBourse.objects.filter(Q(submit_fichier=True)&Q(id_Emp__in=employee_ids_in_same_department)&Q(Reponse_DRH=True))

    serializer=serializers.DepFichierSerializer(files_in_same_department,many=True)
    for data in serializer.data:
        emp=models.Employee.objects.get(id=data['id_Emp'])
        nom=emp.first_name+' '+emp.last_name
        data['nom']=nom
    return Response(serializer.data)




@api_view(['GET'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated]) 
def parcours(request,pk):
    parcours=models.ParcoursProf.objects.filter(id_Emp=pk)
    serializer=serializers.FichierSerializer2(parcours,many=True)
    return Response(serializer.data)

@api_view(['GET'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated]) 
def GetUsers(request):
    if request.user.is_superuser:
        users=models.Employee.objects.all()
        serializer=serializers.EmployeeSerializer(users,many=True)
        return Response(serializer.data)
    return Response({'u r not superuser'})


@api_view(['PUT'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated])
def PutUsers(request,pk):
    if request.user.is_superuser:
        user=models.Employee.objects.get(id=pk)
        data=request.data
        serializer=serializers.EmployeeSerializer(user,data=data)
        if serializer.is_valid():
            serializer.save()
            data=serializer.data
            if data['is_commission']:
                print("tarek")
                send_email(user.email,"New Roll","You are now Commission Chef")
            elif data['is_departement']:    
                send_email(user.email,"New Roll","You are now Departement Chef")
            elif data['is_stricture']:
                send_email(user.email,"New Roll","You are now Diraction Chef")
            elif data['is_superuser']:
                send_email(user.email,"New Roll","You are now DRH Membre")
            else :
                send_email(user.email,"New Roll","You are now simple Employee")

            # if is_commission is_departement is_stricture is_superuser
            return Response(serializer.data)
        return Response(serializer.errors)
    return Response({'u r not superuser'})




@api_view(['PUT'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated])
def PutFileByDep(request,pk):
    data=request.data
    data=data['data']
    fichier=get_object_or_404(models.FichierBourse,id=pk)
    fichier.response_Dep=True
    fichier.NomRespo=data['NomRespo']
    fichier.PrenomRespo=data['PrenomRespo']
    fichier.fanction=data['fanction']
    fichier.CompetanceRespo=data['CompetanceRespo']
    fichier.Commentaire=data['Commentaire']
    fichier.favorable=data['favorable']
    fichier.response_Dep=True
    fichier.save()
    return Response({'done!!!!!'})


@api_view(['GET'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated]) 
def GetFileDrh_Satisfie(request):
    files=models.FichierBourse.objects.all()
    serializer=serializers.DepFichierSerializer(files,many=True)
    for data in serializer.data:
        emp=models.Employee.objects.get(id=data['id_Emp'])
        nom=emp.first_name+' '+emp.last_name
        data['nom']=nom
    print(serializer.data)
    return Response(serializer.data)


@api_view(['GET'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated]) 
def GetFileDrh_Cree_Comm(request):
    files=models.FichierBourse.objects.filter(response_Dep=True,id_comm=None)
    serializer=serializers.DepFichierSerializer(files,many=True)
    for data in serializer.data:
        emp=models.Employee.objects.get(id=data['id_Emp'])
        nom=emp.first_name+' '+emp.last_name
        data['nom']=nom
    print(serializer.data)
    return Response(serializer.data)




@api_view(['GET'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated]) 
def Get_Comm(request):
    users=models.Employee.objects.filter(is_commission=True)
    serializer=serializers.EmployeeSerializer(users,many=True)
    return Response(serializer.data)


@api_view(['PUT'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated])
def Add_comm(request,pk):
    data=request.data
    data=data['data']
    fichier=get_object_or_404(models.FichierBourse,id=pk)
    id_user=data['id_comm']
    user=models.Employee.objects.get(id=id_user)

    fichier.id_comm=user
    fichier.save()
    return Response({'done!!!!!'})

@api_view(['PUT'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated])
def Set_satisfie(request,pk):
    data=request.data
    data=data['data']
    fichier=get_object_or_404(models.FichierBourse,id=pk)
    user=models.Employee.objects.get(id=fichier.id_Emp.id)
    fichier.Reponse_DRH=data['Reponse_DRH']
    if data['Reponse_DRH']==False:

        fichier.allright=False

    fichier.save()
    if data['Reponse_DRH']:
        send_email(user.email,'Etat File','Your File is statisfied')
    else:
        send_email(user.email,'Etat File','Your File is Not statisfied')
    return Response({'done!!!!!'})




@api_view(['GET'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated]) 
def Get_File_for_Com(request):
    user=request.user
    files=models.FichierBourse.objects.filter(id_comm=user.id)
    serializer=serializers.DepFichierSerializer(files,many=True)
    for data in serializer.data:
        emp=models.Employee.objects.get(id=data['id_Emp'])
        nom=emp.first_name+' '+emp.last_name
        data['nom']=nom
    return Response(serializer.data)

@api_view(['PUT'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated])
def PutFileByCom(request,pk):
    data=request.data
    data=data['data']
    fichier=get_object_or_404(models.FichierBourse,id=pk)
    user=models.Employee.objects.get(id=fichier.id_Emp)
    fichier.Reponse_commesion=data['Reponse_commesion']
    if data['Reponse_commesion']==False:
        fichier.allright=False
    fichier.save()
    if data['Reponse_commesion']:
        send_email(user.email,'Etat File','Your File accepted By Commission')
    else:
        send_email(user.email,'Etat File','Your File not accepted By Commission')

    return Response({'done!!!!!'})



@api_view(['GET'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated]) 
def Get_File_for_Dir(request):
    files=models.FichierBourse.objects.exclude(Reponse_commesion=None)
    offers=models.OffreEMP.objects.filter(Id_struc=request.user.Id_struc)
    print(offers)
    files=files.filter(id_Offre__in=offers)
    serializer=serializers.DepFichierSerializer(files,many=True)
    for data in serializer.data:
        emp=models.Employee.objects.get(id=data['id_Emp'])
        nom=emp.first_name+' '+emp.last_name
        data['nom']=nom
    return Response(serializer.data)

@api_view(['PUT'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated])
def PutFileByDir(request,pk):
    data=request.data
    data=data['data']
    fichier=get_object_or_404(models.FichierBourse,id=pk)
    user=models.Employee.objects.get(id=fichier.id_Emp)
    
    fichier.response_Dir=data['response_Dir']
    fichier.allright=data['response_Dir']
    fichier.save()
    if data['response_Dir']:
        send_email(user.email,'Etat File','Your File accepted By Diraction')
    else:
        send_email(user.email,'Etat File','Your File not accepted By Diraction')

    return Response({'done!!!!!'})

@api_view(['GET'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated])
def FileForEmp(request):
    files=models.FichierBourse.objects.filter(id_Emp=request.user.id)
    serializer=serializers.FichierSerializer(files,many=True)
    # for data in serializer.data:
    #     emp=models.Employee.objects.get(id=data['id_Emp'])
    #     nom=emp.first_name+' '+emp.last_name
    #     data['nom']=nom
    return Response(serializer.data)

@api_view(['GET'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated])
def ProfileData(request):
    user=models.Employee.objects.get(id=request.user.id)
    serializer=serializers.UserSerializer(user)
    return Response(serializer.data)

@api_view(['PUT'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated])
def EditProfile(request):
    user=models.Employee.objects.get(id=request.user.id)
    data=request.data
    if(request.data["Photo"]):
        serializer=serializers.EditUserSerializer1(user,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  
    serializer=serializers.EditUserSerializer2(user,data=data)
    if serializer.is_valid():
       serializer.save()
       return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  
    
@api_view(['Get'])  # Use the appropriate HTTP method for your API
@permission_classes([IsAuthenticated])
def tryToken(request):
    return Response({'tarek'})