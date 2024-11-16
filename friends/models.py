from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Friendlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users')
    friends = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.user.username} Friends list'
    
    def add_friend(self, account):
        if account not in self.friends.all():
            self.friends.add(account)
            self.save()
    
    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()
    
    def unfriend_user(self, removee):
        """
        Initiate the action of unfriending someone
        """
        #removing the friend from the requester
        requester_friendlist = self
        requester_friendlist.remove_friend(removee)
        #removing the requester from the removee friend list
        removee_friendlist = Friendlist.objects.get(user=removee)
        removee_friendlist.remove_friend(requester_friendlist.user)

    
    def is_mutual_friend(self,friend):
       "Is the current user friend with the other"
       if friend in self.friends.all():
           return True
       else:
           return False
       
class FriendRequest(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE, related_name='receiver')
    is_active = models.BooleanField(default=True, blank=True, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} friend request to {self.receiver.username}'
    
    def accept(self):
        """
        Both sender and receiver will now be friends
        """
        receiver_friend_list = Friendlist.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = Friendlist.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()
    
    def decline(self):
        """
        Decline a friend request.
        It is 'declined' by setting the 'is_active' to false
        """
        self.is_active = False
        self.save()

    def cancel(self):
        """
        cancel a friend request
        It is 'cancel' by setting the 'is_active' to false
        The difference to declining is that it's the sender that does it
        """
        self.is_active = False
        self.save()