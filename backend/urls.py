from django.contrib import admin
from django.urls import path, include
from allauth.account.views import LoginView, SignupView 
from api.views import check_role

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(template_name='auth.html'), name='account_login'),
    path('accounts/signup/', SignupView.as_view(template_name='auth.html'), name='account_signup'),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', check_role),  
    path('', include('api.urls')), 
]