from django.urls import path 

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('chat/<int:id>/', views.Chat.as_view(), name='chat'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('main/', views.Main.as_view(), name='main'),
    path('logout/', views.Logout.as_view(), name='logout'),
    
]