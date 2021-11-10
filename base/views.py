from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.db.models import Q
from .models import Room,Topic
from django.contrib.auth.models import User
from .forms import RoomForm

# Create your views here.

# rooms = [
#     {"id" : 1, "name": "Let's learn Python"},
#     {"id" : 2, "name": "Let's learn GIT"},
#     {"id" : 3, "name": "Let's learn JavaScript"},
#     {"id" : 4, "name": "Let's learn Angular"},
# ]

def loginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist !")

        user = authenticate(request, username=username, password=password)

        if user != None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password are incorrect !")
    context = {}

    return render(request, "base/auth.html", context)

def logoutView(request):

    logout(request)
    return redirect("login")

def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    rooms = Room.objects.filter(
        Q(topic__title__icontains=q) |
        Q(title__icontains=q) |
        Q(description__icontains=q)
        )
    rooms_count = rooms.count()
    topics = Topic.objects.all()
    context = {
        "rooms" : rooms, 
        "topics" : topics,
        "rooms_count" : rooms_count
        }
    return render(request, "base/home.html", context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room" : room}
    return render(request, "base/room.html", context)

def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form" : form}
    return render(request, "base/room_form.html", context)

def editRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form" : form}
    return render(request, "base/room_form.html", context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == "POST": # Check if it's a POST request
        room.delete()
        return redirect("home")

    return render(request, "base/delete.html", {"obj" : room})