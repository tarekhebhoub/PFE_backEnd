from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('sign-up/',views.EmployeeCreate.as_view()),
    path('structure/',views.StructureView.as_view()),
    path('structure/<int:pk>/',views.DepartementView.as_view()),
    path('logout/',views.LogoutView.as_view()),
    path('login/',views.LoginView.as_view()),
    path('OffreEmp/',views.OffrelistView.as_view()),
    path('OffreEmp/<int:pk>/',views.OffreView.as_view()),
    path('fichier/',views.FichierListView.as_view()),
    path('fichier/<int:pk1>/',views.FichierView.as_view()),
    path('submitFile/<int:pk>/',views.fileSubmit),
    path('fichier/<int:pk>/FichierB/',views.get, name='FichierB'),
    path('parcoursprof/',views.TableListe.as_view()),
    path('parcoursprof/<int:pk1>/',views.Table.as_view()),
    path('resume/',views.Resume),
    path('fileforDep/',views.FileForDep),
    path('parcours/<int:pk>/',views.parcours),
    path('users/',views.GetUsers),
    path('resume/<int:pk>/',views.resumePK),
    path('departement/',views.Departements.as_view()),
    path('userID/<int:pk>/',views.PutUsers),
    path('filePutDep/<int:pk>/',views.PutFileByDep),
    path('fileforDrh_Satisfie/',views.GetFileDrh_Satisfie),
    path('set_satisfie/<int:pk>/',views.Set_satisfie),
    path('fileforDRH_Cree_Com/',views.GetFileDrh_Cree_Comm),
    path('users_comm/',views.Get_Comm),
    path('set_com_fichier/<int:pk>/',views.Add_comm),
    path('fileforCom/',views.Get_File_for_Com),
    path('filePutCom/<int:pk>/',views.PutFileByCom),
    path('fileforDir/',views.Get_File_for_Dir),
    path('filePutDir/<int:pk>/',views.PutFileByDir),
    path('file_for_emp/',views.FileForEmp)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)