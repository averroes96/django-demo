from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

# Create your views here.

rooms = [
    {"id" : 1, "name": "Let's learn Python"},
    {"id" : 2, "name": "Let's learn GIT"},
    {"id" : 3, "name": "Let's learn JavaScript"},
    {"id" : 4, "name": "Let's learn Angular"},
]


def home(request):
    rooms = Room.objects.all()
    context = {"rooms" : rooms}
    return render(request, "base/home.html", context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room" : room}
    return render(request, "base/room.html", context)

def createRoom(request):
    context = {}
    return render(request, "base/room_form.html", context)
