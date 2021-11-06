from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

rooms = [
    {"id" : 1, "name": "Let's learn Python"},
    {"id" : 2, "name": "Let's learn GIT"},
    {"id" : 3, "name": "Let's learn JavaScript"},
    {"id" : 4, "name": "Let's learn Angular"},
]

def home(request):
    context = {"rooms" : rooms}
    return render(request, "base/home.html", context)

def room(request, pk):
    chosen_room = None
    for room in rooms:
        if room["id"] == int(pk):
            chosen_room = room
            break
    context = {"room" : chosen_room}
    return render(request, "base/room.html", context)
