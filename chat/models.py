from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os

class PublicChatRoom(models.Model):
    name = models.CharField(max_length=30,unique=True)
    public = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.name
    
class Message(models.Model):
    room = models.ForeignKey(PublicChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True,null=True)
    file = models.ImageField( blank=True, null=True, upload_to='files/')
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def file_name(self):
        if self.file != None:
            return os.path.basename(self.file.name)
        else:
            return None
        
    def __str__(self):
        if self.content:
            return self.content
        if self.file != None:
            return self.file_name
    
    def save(self, *args, **kwargs):
        #this method is used to resize the uploaded image
        super(Message, self).save(*args, **kwargs)
        
        #This open the image
       
        try:
            if self.file != None :
                img = Image.open(self.file.path)
                if img.height > 250 or img.width > 250:
                    output_size = (250,250)
                    img.thumbnail(output_size)
                    img.save(self.file.path)
        except:
            pass
        
class PrivateChatRoom(models.Model):
    name = models.CharField(max_length=30,blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, blank=True, related_name='members')
    def __str__(self):
        if self.name:
            return self.name
        else:
            return f"{self.creator.username} private chat"
        
class PrivateMessage(models.Model):
    room = models.ForeignKey(PrivateChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True,null=True)
    file = models.ImageField( blank=True, null=True, upload_to='files/')
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def file_name(self):
        if self.file != None:
            return os.path.basename(self.file.name)
        else:
            return None
        
    def __str__(self):
        if self.content:
            return self.content
        if self.file != None:
            return self.file_name
    
    def save(self, *args, **kwargs):
        #this method is used to resize the uploaded image
        super(PrivateMessage, self).save(*args, **kwargs)
        
        #This open the image
       
        try:
            if self.file != None :
                img = Image.open(self.file.path)
                if img.height > 250 or img.width > 250:
                    output_size = (250,250)
                    img.thumbnail(output_size)
                    img.save(self.file.path)
        except:
            pass