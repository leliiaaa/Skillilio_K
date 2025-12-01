from django.urls import path, include
from . import views
from allauth.account.views import LoginView, SignupView 

urlpatterns = [
    path('', views.index, name='home'),
    path('accounts/login/', LoginView.as_view(template_name='auth.html'), name='account_login'),
    path('accounts/signup/', SignupView.as_view(template_name='auth.html'), name='account_signup'),
    path('auth/', views.auth_page, name='auth'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('select-role/', views.select_role, name='select_role'),
    path('check-role/', views.check_role, name='check_role'),
    path('save-role/<str:role_type>/', views.save_role, name='save_role'),
    path('accounts/profile/', views.check_role, name='profile_redirect'), 
    path('create-order/', views.create_order, name='create_order'),
    path('settings/', views.settings_page, name='settings'), 
    path('inbox/', views.inbox, name='inbox'),
    path('chat/<int:user_id>/', views.chat_room, name='chat_room'), 
    path('edit-order/<int:order_id>/', views.edit_order, name='edit_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/apply/', views.ai_interview_start, name='ai_interview'),  
    path('fake-login/<str:provider>/', views.fake_social_login, name='fake_social_login'),
    path('finance/deposit/', views.finance_deposit, name='finance_deposit'),
    path('finance/withdraw/', views.finance_withdraw, name='finance_withdraw'),
    path('finance/transfer/', views.finance_transfer, name='finance_transfer'),
    path('order/<int:order_id>/check/', views.ai_interview_check, name='ai_interview_check'),
]