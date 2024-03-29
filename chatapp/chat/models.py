from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='media', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username


# class ChatRoom(models.Model): #model for Groupchats
#     room_name = models.CharField(max_length=100)
#     description = models.CharField(max_length=200)
#     group_members = models.ManyToManyField(User,related_name='chat_room')

#     def __str__(self):
#         return self.room_name
    

class DirectMessage(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="send_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    file = models.FileField(upload_to='media', blank=True, null=True)
    file_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
            return f"{self.sender.username} -> {self.recipient.username}"
    

class Group(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(User, related_name="group_users")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class GroupChat(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sent_group_messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.sender.username} - {self.group.name}'
    
    
    
    

