from django.shortcuts import render,redirect
from app_modules.adminapp import forms
from app_modules.adminapp import models
from django.http import HttpResponse
from app_modules.userapp.models import CustomUser

from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate

# Create your views here.

def forms_view(request):
    return render(request,'adminapp/forms.html')

def analytics_view(request):
    return render(request,'adminapp/analytics.html')




def index1_view(request):
    from app_modules.userapp.models import CustomUser, PlayerRequest, TournamentRegistration
    from app_modules.adminapp.models import player, team, tournament, match
    
    total_users = CustomUser.objects.count()
    total_players = player.objects.count()
    total_teams = team.objects.count()
    total_tournaments = tournament.objects.count()
    total_matches = match.objects.count()
    
    pending_approvals = PlayerRequest.objects.filter(status='pending').count()
    
    recent_users = CustomUser.objects.all().order_by('-id')[:5]
    recent_registrations = TournamentRegistration.objects.all().order_by('-id')[:5]

    context = {
        'total_users': total_users,
        'total_players': total_players,
        'total_teams': total_teams,
        'total_tournaments': total_tournaments,
        'total_matches': total_matches,
        'pending_approvals': pending_approvals,
        'recent_users': recent_users,
        'recent_registrations': recent_registrations,
    }
    return render(request, 'adminapp/index1.html', context)

def payment_view(request):
    from app_modules.userapp.models import TournamentRegistration
    
    registrations = TournamentRegistration.objects.all().order_by('-registration_date')
    completed_payments = registrations.filter(payment_status='completed')
    
    # Calculate total revenue
    total_revenue = sum(reg.tournament.entry_fee for reg in completed_payments)
    
    context = {
        'registrations': registrations,
        'total_revenue': total_revenue,
        'completed_count': completed_payments.count(),
        'pending_count': registrations.filter(payment_status='pending').count(),
    }
    return render(request, 'adminapp/payment.html', context)





def create_sport(request):
    if request.method == "POST":
        form = forms.sport_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_sport)
        else:
            print(form.errors)
    return render(request,'adminapp/create_sport.html')

def list_sport(request):
    sport = models.sport.objects.all()
    context = {'sport':sport}
    return render(request,'adminapp/list_sport.html',context)

def update_sport(request,id):
    sport = models.sport.objects.get(id=id)
    if request.method == 'POST':
        form = forms.sport_form(request.POST,instance=sport)
        if form.is_valid():
            form.save()
            return redirect(list_sport)
        else:
            print(form.errors)
    context = {'sport':sport}
    return render(request,'adminapp/update_sport.html',context)

def delete_sport(request,id):
    sport = models.sport.objects.get(id=id)
    sport.delete()
    return redirect(list_sport)



#-------------------------------------------------------------------------------------------



def create_team(request):
    sport = models.sport.objects.all()
    if request.method == "POST":
        form = forms.team_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_team)
        else:
            print(form.errors)
    context = {'sport':sport}
    return render(request,'adminapp/create_team.html',context)    

def list_team(request):
    team = models.team.objects.all()
    context = {'team':team}
    return render(request,'adminapp/list_team.html',context)

def update_team(request,id):
    sport = models.sport.objects.all()
    team = models.team.objects.get(id=id)
    if request.method == 'POST':
        form = forms.team_form(request.POST,instance=team)
        if form.is_valid():
            form.save()
            return redirect(list_team)
        else:
            print(form.errors)
    context = {'team':team,'sport':sport}
    return render(request,'adminapp/update_team.html',context)

def delete_team(request,id):
    team = models.team.objects.get(id=id)
    team.delete()
    return redirect(list_team)
    
    
#----------------------------------------------------------------------------------------------


def create_player(request):
    team = models.team.objects.all()
    if request.method == "POST":
        form = forms.player_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_player)
        else:
            print(form.errors)
    context = {'team':team}
    return render(request,'adminapp/create_player.html', context)

def list_player(request):
    player = models.player.objects.all()
    context = {'player':player}
    return render(request,'adminapp/list_player.html',context)

def update_player(request,id):
    team =models.team.objects.all()
    player = models.player.objects.get(id=id)
    if request.method == 'POST':
        form = forms.player_form(request.POST,instance=player)
        if form.is_valid():
            form.save()
            return redirect(list_player)
        else:
            print(form.errors)
    context = {'player':player, 'team':team}
    return render(request,'adminapp/update_player.html',context)

def delete_player(request,id):
    player = models.player.objects.get(id=id)
    player.delete()
    return redirect(list_player)

#---------------------------------------------------------------------------------------------

def list_player_request(request):
    from app_modules.userapp.models import PlayerRequest
    reqs = PlayerRequest.objects.all().order_by('-created_at')
    context = {'reqs': reqs}
    return render(request, 'adminapp/list_player_request.html', context)

def approve_player_request(request, id):
    from app_modules.userapp.models import PlayerRequest
    req = PlayerRequest.objects.get(id=id)
    req.status = 'accepted'
    req.save()
    return redirect('list_player_request')

def reject_player_request(request, id):
    from app_modules.userapp.models import PlayerRequest
    req = PlayerRequest.objects.get(id=id)
    req.status = 'rejected'
    req.save()
    return redirect('list_player_request')

#---------------------------------------------------------------------------------------------


def create_tournament(request):
    sport = models.sport.objects.all()
    if request.method == "POST":
        form = forms.tournament_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_tournament)
        else:
            print(form.errors)
    context = {'sport':sport}
    return render(request,'adminapp/create_tournament.html',context)

def list_tournament(request):
    tournament = models.tournament.objects.all()
    context = {'tournament':tournament}
    return render(request,'adminapp/list_tournament.html',context)

def update_tournament(request,id):
    sport = models.sport.objects.all()
    tournament = models.tournament.objects.get(id=id)
    if request.method == 'POST':
        form = forms.tournament_form(request.POST,instance=tournament)
        if form.is_valid():
            form.save()
            return redirect(list_tournament)
        else:
            print(form.errors)
    context = {'tournament':tournament, 'sport':sport}
    return render(request,'adminapp/update_tournament.html',context)

def delete_tournament(request,id):
    tournament = models.tournament.objects.get(id=id)
    tournament.delete()
    return redirect(list_tournament)


#-------------------------------------------------------------------------------------------------------

def create_match(request):
    tournament = models.tournament.objects.all()
    if request.method == "POST":
        form = forms.match_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_match)
        else:
            print(form.errors)
    context ={'tournament':tournament}
    return render(request,'adminapp/create_match.html', context)

def list_match(request):
    match = models.match.objects.all()
    context = {'match':match}
    return render(request,'adminapp/list_match.html',context)

def update_match(request,id):
    tournament = models.tournament.objects.all()
    match = models.match.objects.get(id=id)
    if request.method == 'POST':
        form = forms.match_form(request.POST,instance=match)
        if form.is_valid():
            form.save()
            return redirect(list_match)
        else:
            print(form.errors)
    context = {'match':match,'tournament':tournament}
    return render(request,'adminapp/update_match.html',context)

def delete_match(request,id):
    match = models.match.objects.get(id=id)
    match.delete()
    return redirect(list_match)

#----------------------------------------------------------------------------------------------------------

def create_playerperformance(request):
    player = models.player.objects.all()
    # match = models.match.objects.all()
    if request.method == "POST":
        form = forms.playerperformance_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_playerperformance)
        else:
            print(form.errors)
    context = {'player':player}
    return render(request,'adminapp/create_playerperformance.html',context)

def list_playerperformance(request):
    playerperformance = models.playerperformance.objects.all()
    context = {'playerperformance':playerperformance}
    return render(request,'adminapp/list_playerperformance.html',context)

def update_playerperformance(request,id):
    player = models.player.objects.all()
    playerperformance = models.playerperformance.objects.get(id=id)
    if request.method == 'POST':
        form = forms.playerperformance_form(request.POST,instance=playerperformance)
        if form.is_valid():
            form.save()
            return redirect(list_playerperformance)
        else:
            print(form.errors)
    context = {'playerperformance':playerperformance,'player':player}
    return render(request,'adminapp/update_playerperformance.html',context)


def delete_playerperformance(request,id):
    playerperformance = models.playerperformance.objects.get(id=id)
    playerperformance.delete()
    return redirect(list_playerperformance)

#---------------------------------------------------------------------------------

def create_announcement(request):
    tournament = models.tournament.objects.all()
    if request.method == "POST":
        form = forms.announcement_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_announcement)
        else:
            print(form.errors)
    context = {'tournament':tournament}
    return render(request,'adminapp/create_announcement.html',context)

def list_announcement(request):
    announcement = models.announcement.objects.all()
    context = {'announcement':announcement}
    return render(request,'adminapp/list_announcement.html',context)

def update_announcement(request,id):
    tournament = models.tournament.objects.all()
    announcement = models.announcement.objects.get(id=id)
    if request.method == 'POST':
        form = forms.announcement_form(request.POST,instance=announcement)
        if form.is_valid():
            form.save()
            return redirect(list_announcement)
        else:
            print(form.errors)
    context = {'announcement':announcement,'tournament':tournament}
    return render(request,'adminapp/update_announcement.html',context)

def delete_announcement(request,id):
    announcement = models.announcement.objects.get(id=id)
    announcement.delete()
    return redirect(list_announcement)

#---------------------------------------------------------------------------------

def list_tournament_registration(request):
    from app_modules.userapp.models import TournamentRegistration
    registrations = TournamentRegistration.objects.all().order_by('-registration_date')
    context = {'registrations': registrations}
    return render(request, 'adminapp/list_tournament_registration.html', context)
