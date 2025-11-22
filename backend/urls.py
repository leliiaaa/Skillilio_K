from django.contrib import admin
from django.urls import path, include  

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Вхід через соцмережі 
    path('accounts/', include('allauth.urls')),
    
    # головна сторінка
    path('', include('api.urls')), 
]