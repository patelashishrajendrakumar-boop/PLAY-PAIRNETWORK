from django import forms
from app_modules.adminapp import models

class sport_form(forms.ModelForm):
    class Meta:
        model = models.sport
        fields = '__all__'
        
class team_form(forms.ModelForm):
    class Meta:
        model = models.team
        fields = '__all__'
        
class player_form(forms.ModelForm):
    class Meta:
        model = models.player
        fields = '__all__'
        
        
class tournament_form(forms.ModelForm):
    class Meta:
        model = models.tournament
        fields = '__all__'
        
class match_form(forms.ModelForm):
    class Meta:
        model = models.match
        fields = '__all__'
        
class playerperformance_form(forms.ModelForm):
    class Meta:
        model = models.playerperformance
        fields = '__all__'
        
class announcement_form(forms.ModelForm):
    class Meta:
        model = models.announcement
        fields = '__all__'