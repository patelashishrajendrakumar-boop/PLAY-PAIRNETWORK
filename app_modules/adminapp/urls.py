from django.contrib import admin
from django.urls import path,include
from app_modules.adminapp import views

urlpatterns = [
    path('forms_view/',views.forms_view,name="forms_view"),
    path('analytics_view/',views.analytics_view,name="analytics_view"),

    
    path('index1_view/',views.index1_view,name="index1_view"),
    
    
    path('payment_view/',views.payment_view,name="payment_view"),
    
    


    path('create_sport/',views.create_sport,name="create_sport"),
    path('list_sport/',views.list_sport,name="list_sport"),
    path('update_sport/<int:id>/',views.update_sport,name="update_sport"),
    path('delete_sport/<int:id>/',views.delete_sport,name="delete_sport"),
    
    path('create_team/',views.create_team,name="create_team"),
    path('list_team/',views.list_team,name="list_team"),
    path('update_team/<int:id>/',views.update_team,name="update_team"),
    path('delete_team/<int:id>/',views.delete_team,name="delete_team"),
    
    path('create_player/',views.create_player,name="create_player"),
    path('list_player/',views.list_player,name="list_player"),
    path('update_player/<int:id>/',views.update_player,name="update_player"),
    path('delete_player/<int:id>/',views.delete_player,name="delete_player"),

    path('list_player_request/', views.list_player_request, name="list_player_request"),
    path('approve_player_request/<int:id>/', views.approve_player_request, name="approve_player_request"),
    path('reject_player_request/<int:id>/', views.reject_player_request, name="reject_player_request"),
    
    
    path('create_tournament/',views.create_tournament,name="create_tournament"),
    path('list_tournament/',views.list_tournament,name="list_tournament"),
    path('update_tournament/<int:id>/',views.update_tournament,name="update_tournament"),
    path('delete_tournament/<int:id>/',views.delete_tournament,name="delete_tournament"),




    
    
    path('create_match/',views.create_match,name="create_match"),
    path('list_match/',views.list_match,name="list_match"),
    path('update_match/<int:id>/',views.update_match,name="update_match"),
    path('delete_match/<int:id>/',views.delete_match,name="delete_match"),
    
    
    path('create_playerperformance/',views.create_playerperformance,name="create_playerperformance"),
    path('list_playerperformance/',views.list_playerperformance,name="list_playerperformance"),
    path('update_playerperformance/<int:id>/',views.update_playerperformance,name="update_playerperformance"),
    path('delete_playerperformance/<int:id>/',views.delete_playerperformance,name="delete_playerperformance"),
    
    
    path('create_announcement/',views.create_announcement,name="create_announcement"),
    path('list_announcement/',views.list_announcement,name="list_announcement"),
    path('update_announcement/<int:id>/',views.update_announcement,name="update_announcement"),
    path('delete_announcement/<int:id>/',views.delete_announcement,name="delete_announcement"),
    
    path('list_tournament_registration/', views.list_tournament_registration, name="list_tournament_registration"),
       
]