from django.db import models
from django.utils import timezone

# Create your models here.
class sport(models.Model):
    
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    
class team(models.Model):
    name = models.CharField(max_length=255)
    sport = models.ForeignKey(sport,on_delete=models.CASCADE)
    coach = models.CharField(max_length=222)
    logo = models.FileField(upload_to='team_image')
    established_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=222)
    created_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class player(models.Model):
    name = models.CharField(max_length=234)
    sport = models.ForeignKey(sport, on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey(team,on_delete=models.CASCADE, null=True, blank=True)
    photo = models.FileField(upload_to='player_image')
    jersey_number = models.IntegerField()
    position = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    total_matches = models.IntegerField()
    total_score = models.IntegerField()
    created_at = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.name

class tournament(models.Model):
    name = models.CharField(max_length=222)
    sport = models.ForeignKey(sport,on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=221)
    prize = models.IntegerField()
    description = models.CharField(max_length=222)
    total_teams = models.IntegerField(default=16)
    entry_fee = models.IntegerField(default=0)
    created_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
   
class match(models.Model):
    tournament = models.ForeignKey(tournament,on_delete=models.CASCADE)
    team_one = models.CharField(max_length=222)
    team_two = models.CharField(max_length=111)
    match_date = models.DateField(null=True, blank=True)
    venue = models.CharField(max_length=88)
    team_one_score = models.IntegerField()
    team_two_score = models.IntegerField()
    is_completed = models.CharField(max_length=222)
    created_at  = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.team_one} vs {self.team_two}"
     
     
class playerperformance(models.Model):
    player = models.ForeignKey(player,on_delete=models.CASCADE)
    match = models.IntegerField()
    score = models.IntegerField()
    assists = models.CharField(max_length=99)
    fouls = models.IntegerField()
    minutes_played = models.TimeField()
    created_at  = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.player.name} - Match {self.match}"
    
class announcement(models.Model):
    title = models.CharField(max_length=255)
    message = models.CharField(max_length=179)
    tournament = models.ForeignKey(tournament,on_delete=models.CASCADE)
    is_active = models.CharField(max_length=222)
    created_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

    