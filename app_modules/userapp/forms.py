from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, TournamentRegistration
from app_modules.adminapp.models import player, team, sport


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    game = forms.CharField(max_length=100, label="Select Game", required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Sport Name'}))
    jersey_number = forms.IntegerField(required=True)
    total_matches = forms.IntegerField(label="Total Matches", required=True)
    total_score = forms.IntegerField(label="Total Score", required=True)
    position = forms.CharField(max_length=50, required=True)
    height = forms.FloatField(required=True)
    weight = forms.FloatField(required=True)
    photo = forms.ImageField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'phone_number',
            'date_of_birth',
            'gender',
            'address'
        ]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken!")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered!")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = self.data.get("password1")
        password2 = self.data.get("password2")

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match!")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'user'
        user.set_password(self.data.get("password1"))
        if 'photo' in self.cleaned_data:
            user.profile_image = self.cleaned_data['photo']
            
        if commit:
            user.save()
            # Automatically create a player profile linked by name
            from app_modules.adminapp.models import sport as SportModel
            game_name = self.cleaned_data['game']
            sport_obj, created = SportModel.objects.get_or_create(name=game_name)

            player.objects.create(
                name=user.username,
                sport=sport_obj,
                photo=self.cleaned_data['photo'],
                jersey_number=self.cleaned_data['jersey_number'],
                position=1, # Default as IntegerField
                height=self.cleaned_data['height'],
                weight=self.cleaned_data['weight'],
                total_matches=self.cleaned_data['total_matches'],
                total_score=self.cleaned_data['total_score']
            )
        return user

class TournamentRegistrationForm(forms.ModelForm):
    class Meta:
        model = TournamentRegistration
        fields = ['player_name', 'team_name', 'jersey_number']
        widgets = {
            'player_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Player Name'}),
            'team_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Team Name'}),
            'jersey_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Jersey Number'}),
        }