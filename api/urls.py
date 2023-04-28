from django.urls import path
from .apiviews import UserCreate, CardView,LoginView, LogoutView,Lock,get_pos,Position,StationsView,StationView,SoldView
urlpatterns = [
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('sign-up/',UserCreate.as_view()),
    path('lock_key/',Lock.as_view()),
    path('pos_users/',get_pos),
    path('pos_user/',Position.as_view()),
    path('stations/',StationsView.as_view()),
    path('stations/<int:pk>',StationView.as_view()),
    path('cards/',CardView.as_view()),
    path('sold/',SoldView.as_view())
]

