from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from app_modules.userapp import models as user_models
from django.contrib.auth.decorators import login_required

from app_modules.adminapp import models as admin_models

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from app_modules.userapp import forms
from django.contrib import messages


# Create your views here.

from django.contrib.auth.decorators import login_required

@login_required
def edit_view(request):
    user = request.user
    player_obj = admin_models.player.objects.filter(name=user.username).first()
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email') 
        user.phone_number = request.POST.get('phone_number')
        user.date_of_birth = request.POST.get('date_of_birth')
        user.bio = request.POST.get('bio')
        
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
            if player_obj:
                player_obj.photo = request.FILES['profile_image']
            
        user.save() 
        
        # Update player profile if it exists
        if player_obj:
            player_obj.total_matches = int(request.POST.get('total_matches', 0))
            player_obj.total_score = int(request.POST.get('total_score', 0))
            
            sport_name = request.POST.get('sport')
            if sport_name:
                sport_obj, created = admin_models.sport.objects.get_or_create(name=sport_name)
                player_obj.sport = sport_obj
            
            player_obj.save()
            
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile_view')  
    
    sports = admin_models.sport.objects.all()
    
    context = {
        'sports': sports,
        'player_obj': player_obj
    }
    return render(request, 'userapp/edit_profile.html', context)


# def dashboard_view(request):
#     from django.db.models import Count
#     from django.utils import timezone
    
#     now = timezone.now().date()
#     first_day_of_month = now.replace(day=1)
    
#     total_players = admin_models.player.objects.count()
#     active_teams = admin_models.team.objects.count()
#     total_tournaments = admin_models.tournament.objects.count()
    
#     # Matches this month
#     matches_this_month = admin_models.match.objects.filter(match_date__gte=first_day_of_month).count()
    
#     # Recent matches
#     recent_matches = admin_models.match.objects.all().order_by('-match_date')[:5]
    
#     # Pending requests (Approvals)
#     pending_approvals = user_models.PlayerRequest.objects.filter(status='pending').order_by('-created_at')[:3]
#     total_pending = user_models.PlayerRequest.objects.filter(status='pending').count()
    
#     # Players by sport (for the donut chart)
#     players_by_sport = admin_models.player.objects.values('sport__name').annotate(count=Count('id'))
#     total_players_with_sport = sum(p['count'] for p in players_by_sport)
    
#     # Top performers (using player objects for now as a placeholder for real performance data)
#     top_performers = admin_models.player.objects.order_by('-total_score')[:4]
    
#     # Attach online status
#     all_users = user_models.CustomUser.objects.all()
#     user_status_map = {u.username: u.is_online() for u in all_users}
#     for p in top_performers:
#         p.is_online = user_status_map.get(p.name, False)
    
#     # Tournament stats
#     active_tournaments = admin_models.tournament.objects.filter(start_date__lte=now, end_date__gte=now).count()
#     upcoming_tournaments = admin_models.tournament.objects.filter(start_date__gt=now).count()

#     # Registered tournaments for the current user
#     my_registrations = user_models.TournamentRegistration.objects.filter(user=request.user).select_related('tournament')
#     my_tournaments = [reg.tournament for reg in my_registrations]

#     context = {
#         'total_players': total_players,
#         'active_teams': active_teams,
#         'total_tournaments': total_tournaments,
#         'matches_this_month': matches_this_month,
#         'recent_matches': recent_matches,
#         'pending_approvals': pending_approvals,
#         'total_pending': total_pending,
#         'players_by_sport': players_by_sport,
#         'total_players_with_sport': total_players_with_sport,
#         'top_performers': top_performers,
#         'active_tournaments': active_tournaments,
#         'upcoming_tournaments': upcoming_tournaments,
#         'my_tournaments': my_tournaments,
#         'now': now,
#     }
#     return render(request, 'userapp/dashboard.html', context)

def index_view(request):
    from django.utils import timezone
    now = timezone.now().date()
    
    # 1. Hero Stats
    total_players = admin_models.player.objects.count()
    total_teams = admin_models.team.objects.count()
    total_tournaments = admin_models.tournament.objects.count()
    total_matches = admin_models.match.objects.count()

    # 2. Latest Matches
    latest_matches = admin_models.match.objects.all().order_by('-match_date')[:3]

    # 3. Announcement
    announcement = admin_models.announcement.objects.filter(is_active='active').last()

    # 4. Top Players
    top_players = admin_models.player.objects.all().order_by('-total_score')[:3]

    context = {
        'total_players': total_players,
        'total_teams': total_teams,
        'total_tournaments': total_tournaments,
        'total_matches': total_matches,
        'latest_matches': latest_matches,
        'announcement': announcement,
        'top_players': top_players,
        'now': now,
    }
    return render(request, 'userapp/index.html', context)

# def login_view(request):
#     return render(request,'userapp/login.html')

def matches_view(request):
    mat = admin_models.match.objects.all()
    for m in mat:
        # Attach team objects to access logos
        m.team_one_obj = admin_models.team.objects.filter(name=m.team_one).first()
        m.team_two_obj = admin_models.team.objects.filter(name=m.team_two).first()
    context = {'mat': mat}
    return render(request,'userapp/matches.html', context)

def players_view(request):
    from django.db.models import Q
    pla = admin_models.player.objects.all()
    
    # 1. KPIs
    total_players = pla.count()
    # Active players: those who are currently online (active in last 5 mins)
    from django.utils import timezone
    import datetime
    threshold = timezone.now() - datetime.timedelta(minutes=5)
    active_players = user_models.CustomUser.objects.filter(last_seen__gt=threshold).count()
    # Pending requests awaiting admin/receiver
    pending_approval = user_models.PlayerRequest.objects.filter(status='pending').count()
    # Top scorers count (players with score > 200 for example)
    top_scorers_count = admin_models.player.objects.filter(total_score__gt=200).count()

    # 2. Filter Options
    sports = admin_models.sport.objects.all()
    teams = admin_models.team.objects.all()

    # 3. Apply Search & Filters
    search_query = request.GET.get('search')
    sport_id = request.GET.get('sport')
    team_id = request.GET.get('team')

    if search_query:
        pla = pla.filter(Q(name__icontains=search_query) | Q(position__icontains=search_query))
    if sport_id:
        pla = pla.filter(sport_id=sport_id)
    if team_id:
        pla = pla.filter(team_id=team_id)

    # Attach online status to each player object
    # We use a dictionary to avoid N+1 queries
    all_users = user_models.CustomUser.objects.all()
    user_status_map = {u.username: u.is_online() for u in all_users}
    for p in pla:
        p.is_online = user_status_map.get(p.name, False)

    # 4. Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(pla, 6) # Show 6 players per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    requested_player_ids = []
    accepted_player_ids = []
    pending_received_count = 0
    
    if request.user.is_authenticated:
        # 1. Requests sent BY the current user
        sent_reqs = user_models.PlayerRequest.objects.filter(sender=request.user)
        requested_player_ids = list(sent_reqs.values_list('receiver_id', flat=True))
        accepted_sent_player_ids = list(sent_reqs.filter(status='accepted').values_list('receiver_id', flat=True))
        
        # 2. Requests received BY the current user's player profile
        current_player = admin_models.player.objects.filter(name=request.user.username).first()
        accepted_received_player_ids = []
        if current_player:
            # Pending count for the notification badge
            pending_received_count = user_models.PlayerRequest.objects.filter(receiver=current_player, status='pending').count()
            
            # Find usernames of people who sent requests to current user and were accepted
            accepted_sender_usernames = user_models.PlayerRequest.objects.filter(
                receiver=current_player, status='accepted'
            ).values_list('sender__username', flat=True)
            
            # Find the player IDs for those usernames to show 'Chat' on their cards
            accepted_received_player_ids = list(admin_models.player.objects.filter(
                name__in=accepted_sender_usernames
            ).values_list('id', flat=True))
            
        accepted_player_ids = accepted_sent_player_ids + accepted_received_player_ids
            
    context = {
        'pla': page_obj, 
        'page_obj': page_obj,
        'sports': sports,
        'teams': teams,
        'total_players': total_players,
        'active_players': active_players,
        'pending_approval': pending_approval,
        'top_scorers_count': top_scorers_count,
        'requested_player_ids': requested_player_ids,
        'accepted_player_ids': accepted_player_ids,
        'pending_received_count': pending_received_count,
        'current_user_name': request.user.username if request.user.is_authenticated else None
    }
    return render(request,'userapp/players.html',context)

@login_required
def my_requests(request):
    # Requests sent BY the user
    sent_reqs = user_models.PlayerRequest.objects.filter(sender=request.user).order_by('-created_at')
    
    # Requests received TO the user's player profile (if they have one)
    received_reqs = []
    current_player = admin_models.player.objects.filter(name=request.user.username).first()
    if current_player:
        received_reqs = user_models.PlayerRequest.objects.filter(receiver=current_player).order_by('-created_at')
        
    context = {
        'sent_reqs': sent_reqs,
        'received_reqs': received_reqs,
        'is_player': current_player is not None
    }
    return render(request, 'userapp/my_requests.html', context)

@login_required
def approve_request(request, request_id):
    req = get_object_or_404(user_models.PlayerRequest, id=request_id)
    # Security check: only the receiver player can approve
    if req.receiver.name == request.user.username:
        req.status = 'accepted'
        req.save()
        messages.success(request, f"Request from {req.sender.username} accepted!")
    else:
        messages.error(request, "Unauthorized action.")
    return redirect('my_requests')

@login_required
def reject_request(request, request_id):
    req = get_object_or_404(user_models.PlayerRequest, id=request_id)
    # Security check: only the receiver player can reject
    if req.receiver.name == request.user.username:
        req.status = 'rejected'
        req.save()
        messages.warning(request, f"Request from {req.sender.username} rejected.")
    else:
        messages.error(request, "Unauthorized action.")
    return redirect('my_requests')

@login_required
def send_request(request, player_id):
    player_obj = get_object_or_404(admin_models.player, id=player_id)
    # Check if a request already exists
    if user_models.PlayerRequest.objects.filter(sender=request.user, receiver=player_obj).exists():
        messages.warning(request, f"You have already sent a request to {player_obj.name}.")
    else:
        user_models.PlayerRequest.objects.create(sender=request.user, receiver=player_obj)
        messages.success(request, f"Request sent to {player_obj.name} successfully!")
    return redirect('players_view')





def teams_view(request):

    tea = admin_models.team.objects.all()
    context = {'tea': tea}
    return render(request,'userapp/teams.html',context)

def tournaments_view(request):
    tour = admin_models.tournament.objects.all()
    if request.user.is_authenticated:
        regs = user_models.TournamentRegistration.objects.filter(user=request.user)
        reg_map = {reg.tournament_id: reg for reg in regs}
        for t in tour:
            t.user_reg = reg_map.get(t.id)
    
    context = {
        'tour': tour,
    }
    return render(request, 'userapp/tournaments.html', context)


@login_required
def tournament_register_view(request, tournament_id):
    tournament_obj = get_object_or_404(admin_models.tournament, id=tournament_id)
    
    # Check if user is already registered
    if user_models.TournamentRegistration.objects.filter(user=request.user, tournament=tournament_obj).exists():
        messages.warning(request, "You are already registered for this tournament.")
        return redirect('tournaments_view')

    # Check if tournament is full
    if tournament_obj.registrations.count() >= tournament_obj.total_teams:
        messages.error(request, "This tournament is already full.")
        return redirect('tournaments_view')

    if request.method == 'POST':
        form = forms.TournamentRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.tournament = tournament_obj
            registration.save()
            messages.success(request, f"Registration submitted! Please complete the payment.")
            return redirect('payment_view', registration_id=registration.id)
    else:
        # Pre-fill player name from user's player profile if it exists
        current_player = admin_models.player.objects.filter(name=request.user.username).first()
        initial_data = {}
        if current_player:
            initial_data = {
                'player_name': current_player.name,
                'jersey_number': current_player.jersey_number,
                'team_name': current_player.team.name if current_player.team else ''
            }
        form = forms.TournamentRegistrationForm(initial=initial_data)

    return render(request, 'userapp/tournament_register.html', {
        'form': form,
        'tournament': tournament_obj
    })


@login_required
def payment_view(request, registration_id):
    registration = get_object_or_404(user_models.TournamentRegistration, id=registration_id, user=request.user)
    
    if registration.payment_status == 'completed':
        messages.info(request, "Payment for this registration is already completed.")
        return redirect('tournaments_view')

    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        
        registration.transaction_id = transaction_id
        registration.payment_method = payment_method
        registration.payment_status = 'completed'  # In a real app, this might be 'pending_verification'
        registration.save()
        
        messages.success(request, f"Payment details submitted for {registration.tournament.name}! Admin will verify shortly.")
        return redirect('tournaments_view')
        
    return render(request, 'userapp/payment.html', {'registration': registration})



def profile_view(request):
    current_player = admin_models.player.objects.filter(name=request.user.username).first()
    
    context = {
        'current_player': current_player,
    }
    return render(request, 'userapp/profile.html', context)




# REGISTER
def register_view(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful!")
            return redirect('login_view')
    else:
        form = forms.RegisterForm()

    return render(request, 'userapp/register.html', {'form': form})


# LOGIN (COMMON)
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.role == 'admin':
                return redirect('index1_view')
            else:
                return redirect('index_view')
        else:
            messages.error(request, "Invalid credentials!")
    return render(request, 'userapp/login.html')

# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login_view')




