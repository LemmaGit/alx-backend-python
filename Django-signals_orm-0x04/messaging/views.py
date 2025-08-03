from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .models import Message
from django.shortcuts import render
@login_required
@require_POST
def delete_user(request):
    request.user.delete()
    return redirect('home')

@login_required
def user_conversations(request):
    messages = Message.objects.filter(
        sender=request.user
    ).select_related('receiver', 'parent_message') \
     | Message.objects.filter(
        receiver=request.user
    ).select_related('sender', 'parent_message')

    messages = messages.prefetch_related('replies').order_by('-timestamp')

    return render(request, 'messaging/conversations.html', {'messages': messages})

@login_required
def unread_inbox(request):
    unread_messages = Message.unread.unread_for_user(request.user).only('id', 'sender', 'content', 'timestamp')
    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})