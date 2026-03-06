from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Views
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # API Endpoints
    path('api/process-command/', views.process_command, name='process_command'),
    path('api/conversation-history/', views.get_conversation_history, name='conversation_history'),
    path('api/conversation/<int:conversation_id>/', views.get_conversation, name='get_conversation'),
    path('api/conversation/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
    path('api/commands/', views.get_user_commands, name='user_commands'),
    path('api/clear-history/', views.clear_history, name='clear_history'),
]
