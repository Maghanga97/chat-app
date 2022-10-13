import imp
from django.shortcuts import render
from .models import Room, Message

# Create your views here.
def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room):
    try:
        room_name = Room.objects.create(name=room)
        room_name.save()
    except:
        pass
    room_name = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_name)[0:5]
    return render(request, 'chat/room.html', {'room':room, 'messages': messages})