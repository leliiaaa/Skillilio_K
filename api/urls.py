from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),       # Головна сторінка 
    path('auth/', views.auth_page, name='auth'), # Сторінка входу 
]