from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(r'api.urls')),
    path('tasks/', include(r'tasks.urls')),
    path('users/', include(r'users.urls'))
]
