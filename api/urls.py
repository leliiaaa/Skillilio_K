from django.urls import path
from . import views
from django.conf import settings       
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
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
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)