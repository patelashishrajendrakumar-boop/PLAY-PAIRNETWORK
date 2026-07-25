from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('<str:username>/', views.chat_with_user, name='chat_with_user'),
    path('<str:username>/delete/', views.delete_chat, name='delete_chat'),
    path('message/delete/<int:message_id>/', views.delete_message, name='delete_message'),
]