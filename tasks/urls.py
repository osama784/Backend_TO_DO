from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_tasks),
    path('create/', views.create_task),
    path('<int:pk>/delete/', views.delete_task),
    path('<int:pk>/update/', views.update_task),

    path('categories/', views.list_category),
    path('categories/create/', views.create_category),
    path('categories/<int:pk>/delete/', views.delete_category),
    path('categories/<int:pk>/update/', views.update_category)

]