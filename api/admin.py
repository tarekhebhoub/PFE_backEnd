from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Employee)
admin.site.register(models.Departement)
admin.site.register(models.Structure)
admin.site.register(models.OffreEMP)
admin.site.register(models.FichierBourse)
admin.site.register(models.ParcoursProf)



