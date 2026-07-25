from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Message
from app_modules.userapp.models import PlayerRequest
from app_modules.adminapp.models import player
from django.db.models import Q

User = get_user_model()

def get_accepted_users(user):
    
    sent_accepted = PlayerRequest.objects.filter(sender=user, status='accepted').values_list('receiver__name', flat=True)
    received_accepted = PlayerRequest.objects.filter(receiver__name=user.username, status='accepted').values_list('sender__username', flat=True)
    
    accepted_usernames = list(sent_accepted) + list(received_accepted)
    accepted_users = User.objects.filter(username__in=accepted_usernames).distinct()
    
    
    for acc_user in accepted_users:
        users = sorted([user.username, acc_user.username])
        room_name = f"{users[0]}_{users[1]}"
        acc_user.last_msg = Message.objects.filter(room_name=room_name).order_by('-timestamp').first()
    
    return accepted_users

@login_required
def chat_home(request):
    accepted_users = get_accepted_users(request.user)
    context = {
        'accepted_users': accepted_users,
    }
    return render(request, 'chat/chat_home.html', context)

@login_required
def chat_with_user(request, username):
    other_user = get_object_or_404(User, username=username)
    accepted_users = get_accepted_users(request.user)
    
    
    users = sorted([request.user.username, other_user.username])
    room_name = f"{users[0]}_{users[1]}"
    
    
    messages = Message.objects.filter(room_name=room_name).order_by('timestamp')
    
    context = {
        'other_user': other_user,
        'room_name': room_name,
        'chat_messages': messages,
        'accepted_users': accepted_users,
    }
    return render(request, 'chat/chat_room.html', context)

@login_required
def delete_chat(request, username):
    other_user = get_object_or_404(User, username=username)
    users = sorted([request.user.username, other_user.username])
    room_name = f"{users[0]}_{users[1]}"
    
    # Delete all messages in this room
    Message.objects.filter(room_name=room_name).delete()
    
    return redirect('chat_with_user', username=username)

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.sender == request.user:
        users = message.room_name.split('_')
        other_username = users[1] if users[0] == request.user.username else users[0]
        message.delete()
        return redirect('chat_with_user', username=other_username)
    return redirect('chat_home')