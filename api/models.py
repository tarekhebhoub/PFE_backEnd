from django.db import models
from django.contrib.auth.models import AbstractUser

class Employee(AbstractUser):
    Photo = models.ImageField(upload_to='images/',null=True)
    Date_Naiss = models.DateField(blank=True,null=True)
    Adresse_perso = models.CharField(max_length=100,null=True)
    Date_Recrut = models.DateField(null=True)
    Poste_actuel = models.CharField(max_length=50,null=True)
    Telephone = models.IntegerField(null=True)
    Id_dep = models.ForeignKey("Departement",on_delete=models.CASCADE,null=True)
    Id_struc=models.ForeignKey("Structure",on_delete=models.CASCADE,null=True)
    Echelle=models.CharField(max_length=20,null=True)
    is_departement=models.BooleanField(default=False)
    is_stricture=models.BooleanField(default=False)
    is_commission=models.BooleanField(default=False)
    def __str__(self):
        return self.username


class Departement(models.Model):
    Nom_dep = models.CharField(max_length=30)
    id_struc = models.ForeignKey("Structure",on_delete=models.CASCADE)
    def __str__(self):
        return self.Nom_dep
class Structure(models.Model):
    Nom_struc = models.CharField(max_length=30,unique=True)
    def __str__(self):
        return self.Nom_struc

class FichierBourse(models.Model):
    Raison_recrut = models.CharField(max_length=300)
    PourPoste = models.CharField(max_length=20)
    Specialite = models.CharField(max_length=40)
    formation_comp = models.CharField(max_length=300)
    seminaire = models.CharField(max_length=100)
    submit_fichier=models.BooleanField(null=True,blank=True)
    Commentaire = models.CharField(max_length=300,null=True,blank=True)
    Reponse_DRH = models.BooleanField(null=True,blank=True)
    Reponse_commesion = models.BooleanField(null=True,blank=True)
    
    Etat_fichier = models.CharField(max_length=30,null=True,blank=True)
    
    id_Offre=models.ForeignKey("OffreEMP",on_delete=models.CASCADE)
    id_Emp = models.ForeignKey("Employee",on_delete=models.CASCADE)
    id_comm = models.ForeignKey("Commesion",on_delete=models.CASCADE,null=True,blank=True)

class ParcoursProf(models.Model):
    Poste_occup = models.CharField(max_length=30)
    Travaux_realises = models.CharField(max_length=100)
    id_Emp = models.ForeignKey("Employee",on_delete=models.CASCADE)
    date_deb = models.DateField()
    date_fin = models.DateField()
    # id_fichier = models.ForeignKey("FichierBourse",on_delete=models.CASCADE,default=0)
# 

class Commesion(models.Model):
    President = models.CharField(max_length=40)  

class OffreEMP(models.Model):
   TitreOffre = models.CharField(max_length=50)
   NombrePoste = models.IntegerField()
   Id_dep = models.ForeignKey("Departement",on_delete=models.CASCADE,null=True)
   Id_struc=models.ForeignKey("Structure",on_delete=models.CASCADE,null=True)
   Description = models.FileField(upload_to='file/')
