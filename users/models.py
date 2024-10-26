from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.
 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to="profile/", default='profile/default.png')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        #this method is used to resize the uploaded image
        super(Profile, self).save(*args, **kwargs)
        
        #This open the image
        img = Image.open(self.pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.pic.path)