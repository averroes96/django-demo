from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

# Create your models here.

class Topic(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return str(self.title)

class Room(models.Model):

    class Meta:
        ordering = ["-updated", "-created"]

    host  = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

class Message(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return str(self.content[0:50])