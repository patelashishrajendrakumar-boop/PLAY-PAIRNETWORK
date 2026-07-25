from django.contrib.auth.models import AbstractUser
from django.db import models
from app_modules.adminapp.models import player, tournament


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    def is_online(self):
        if self.last_seen:
            from django.utils import timezone
            import datetime
            # Consider online if active in the last 5 minutes
            return self.last_seen > timezone.now() - datetime.timedelta(minutes=5)
        return False


    def __str__(self):
        return self.username

class PlayerRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(player, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.sender.username} to {self.receiver.name}"


from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(post_delete, sender=CustomUser)
def delete_player_profile(sender, instance, **kwargs):
    """Delete the player profile when the user is deleted."""
    player.objects.filter(name=instance.username).delete()

class TournamentRegistration(models.Model):
    tournament = models.ForeignKey(tournament, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tournament_registrations')
    player_name = models.CharField(max_length=255)
    team_name = models.CharField(max_length=255)
    jersey_number = models.IntegerField()
    payment_status = models.CharField(max_length=20, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player_name} - {self.tournament.name}"
