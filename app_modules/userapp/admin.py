from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')

admin.site.register(CustomUser, CustomUserAdmin)

from .models import TournamentRegistration, PlayerRequest

class TournamentRegistrationAdmin(admin.ModelAdmin):
    list_display = ('player_name', 'tournament', 'team_name', 'payment_status', 'transaction_id', 'payment_method', 'registration_date')
    list_filter = ('payment_status', 'tournament', 'payment_method')
    search_fields = ('player_name', 'team_name', 'tournament__name', 'transaction_id')

admin.site.register(TournamentRegistration, TournamentRegistrationAdmin)

class PlayerRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at')
    list_filter = ('status',)

admin.site.register(PlayerRequest, PlayerRequestAdmin)


