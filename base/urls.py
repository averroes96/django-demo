from django.urls import path
from . import views

urlpatterns = [

    path("login/", views.loginView, name="login"),
    path("register/", views.registerView, name="register"),
    path("logout/", views.logoutView, name="logout"),

    path('', views.home, name = 'home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>/', views.profileView, name='profile'),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>', views.editRoom, name="update-room"),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),
]