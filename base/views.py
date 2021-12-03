from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Message, Room,Topic
from django.contrib.auth.models import User
from .forms import RoomForm,UserForm

# Create your views here.

def loginView(request):

    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
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

    context = {"page" : page}
    return render(request, "base/auth.html", context)

def registerView(request):

    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occured during registeration")

    return render(request, "base/auth.html", {"form" : form})

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
    rooms_count = rooms.count() # Get query row count
    topics = Topic.objects.all()[:4]
    recent_acts = Message.objects.filter(Q(room__topic__title__icontains=q))

    context = {
        "rooms" : rooms, 
        "topics" : topics,
        "rooms_count" : rooms_count,
        "recent_acts" : recent_acts
        }

    return render(request, "base/home.html", context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    context = {
        "room" : room, 
        "room_messages" : room_messages,
        "participants" : participants
    }

    if request.method == "POST":
        Message.objects.create(
            user = request.user,
            room = room,
            content = request.POST.get("content")
        )
        room.participants.add(request.user)
        return redirect("room", pk=room.id)

    return render(request, "base/room.html", context)

def profileView(request, pk):

    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    recent_acts = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        "user": user, 
        "rooms": rooms, 
        "recent_acts": recent_acts, 
        "topics" : topics
    }

    return render(request, "base/profile.html", context)

@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        # form = RoomForm(request.POST)
        topic_title = request.POST.get("room_topic")
        topic,created = Topic.objects.get_or_create(title=topic_title)

        Room.objects.create(
            host=request.user,
            topic=topic,
            title=request.POST.get("title"),
            description=request.POST.get("description")
        )
        
            # if form.is_valid():
            #     room = form.save(commit=False)
            #     room.host = request.user
            #     room.save()
        return redirect("home")
    context = {"form" : form, "topics" : topics}
    return render(request, "base/room_form.html", context)

@login_required(login_url="login")
def editRoom(request, pk):
    
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("Get the hell out of here!!")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)

        topic_title = request.POST.get("room_topic")
        topic,created = Topic.objects.get_or_create(title=topic_title)

        room.title = request.POST.get("title")
        room.topic = topic
        room.description = request.POST.get("description")

        room.save()

        # if form.is_valid():
        #     form.save()

        return redirect("home")
    context = {"form" : form, "topics" : topics, "room" : room}
    return render(request, "base/room_form.html", context)

@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("Get the hell out of here!!")

    if request.method == "POST": # Check if it's a POST request
        room.delete()
        return redirect("home")

    return render(request, "base/delete.html", {"obj" : room})

@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("Get the hell out of here!!")

    if request.method == "POST": # Check if it's a POST request
        message.delete()
        return redirect("home")

    return render(request, "base/delete.html", {"obj" : message})

@login_required(login_url="login")
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if (request.method == "POST"):
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile", pk=user.id)
    return render(request, "base/update-user.html", {"form": form})

def topicsView(request):

    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.filter(title__icontains=q)
    return render(request, "base/topics.html", {"topics" : topics})

def activitiesView(request):

    activities = Message.objects.all()
    return render(request, "base/activity.html", {"recent_acts" : activities})