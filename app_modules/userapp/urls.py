from django.contrib import admin
from django.urls import path,include
from app_modules.userapp import views

urlpatterns = [
    
    # path('dashboard_view/',views.dashboard_view,name="dashboard_view"),
    path('matches_view/',views.matches_view,name="matches_view"),
    path('players_view/',views.players_view,name="players_view"),
    path('send_request/<int:player_id>/', views.send_request, name='send_request'),
    path('approve_request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject_request/<int:request_id>/', views.reject_request, name='reject_request'),
    path('my_requests/', views.my_requests, name='my_requests'),
    
    path('',views.index_view,name="index_view"),
    
    path('teams_view/',views.teams_view,name="teams_view"),
    path('tournaments_view/',views.tournaments_view,name="tournaments_view"),
    path('tournament_register/<int:tournament_id>/', views.tournament_register_view, name='tournament_register'),
    path('payment/<int:registration_id>/', views.payment_view, name='payment_view'),




    
    path('login_view/',views.login_view,name="login_view"),
    path('register_view/',views.register_view,name="register_view"),
    path('logout_view/',views.logout_view,name="logout_view"),
    
    path('profile_view/',views.profile_view,name="profile_view"),
    
    path('edit_view/',views.edit_view,name="edit_view"),
    
    
]
