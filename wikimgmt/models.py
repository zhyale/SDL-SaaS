from django.db import models
from usermgmt.models import User, Company


class Keyword(models.Model):
    name = models.CharField(max_length=64)


class Wiki(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    contributor = models.ForeignKey(User, blank=True, null=True, related_name='contributor_wikis')
    last_editor = models.ForeignKey(User, blank=True, null=True, related_name='editor_wikis')
    abbr = models.CharField(max_length=64, blank=True, null=True)
    expression = models.CharField(max_length=128)
    description = models.CharField(max_length=1024, blank=True, null=True)
    reference = models.CharField(max_length=256, blank=True, null=True)
    keywords = models.ManyToManyField(Keyword, blank=True)
    company = models.ForeignKey(Company, blank=True, null=True, related_name='company_wikis')
