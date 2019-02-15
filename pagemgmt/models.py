from django.db import models
from usermgmt.models import User


class Page(models.Model):
    title = models.CharField(max_length=256)
    banner_image=models.ImageField(upload_to='upload/images', blank=True, null=True)
    content = models.CharField(max_length=4096)
    author = models.CharField(max_length=32, default='Jane')
    time = models.DateTimeField(auto_now_add=True)
    pseudo_name = models.CharField(max_length=64, unique=True)
    keywords = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    show_in_front = models.BooleanField(default=True)
    show_in_carousel = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    page = models.ForeignKey(Page, related_name='page_comments')
    commenter = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=256)

