from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create_User),
    path('', views.get_User),
    path('login/', views.get_Token)
]