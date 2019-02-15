from django.db import models
from usermgmt.models import User

# Create your models here.
# Private Messages
class Message(models.Model):
    sent_time=models.DateTimeField(auto_now_add=True)
    sender=models.ForeignKey(User, blank=True,null=True, related_name='sender_msgs')
    receiver=models.ForeignKey(User,related_name='receiver_msgs')
    body=models.CharField(max_length=1024,blank=True,null=True)
    viewed=models.BooleanField(default=False)
    sender_delete=models.BooleanField(default=False)
    receiver_delete=models.BooleanField(default=False)
    source=models.ForeignKey('self', blank=True, null=True, default=None, related_name='source_msgs')
    last_reply_time=models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.body

class CircleMessage(models.Model):
    sent_time=models.DateTimeField(auto_now_add=True)
    sender=models.ForeignKey(User, related_name='sender_circle_msgs')
    body=models.CharField(max_length=1024,blank=True,null=True)
    image_link=models.CharField(max_length=512, blank=True,null=True)
    anonymous=models.BooleanField(default=False)
    praised_by=models.ManyToManyField(User, blank=True, related_name='praised_msgs')
    source=models.ForeignKey('self', blank=True, null=True, default=None, related_name='source_circle_msgs')
    last_reply_time=models.DateTimeField(auto_now=True)

    def display_sender(self):
        return self.sender.nickname if self.anonymous else self.sender.username



