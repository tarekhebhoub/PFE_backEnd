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
    path('fichier/<int:pk>/',views.FichierView.as_view()),
    path('fichier/<int:pk>/FichierB/',views.get, name='FichierB'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)