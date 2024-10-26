from django.db import models
from django.contrib.auth.models import User

class PublicChatRoom(models.Model):
    name = models.CharField(max_length=100,unique=True)
    public = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.name

class PrivateChatRoom(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(unique=True)
    #founder = models.ForeignKey(User, on_delete=models.CASCADE)
    Members = models.ManyToManyField(User)
   
class Message(models.Model):
    room = models.ForeignKey(PublicChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
