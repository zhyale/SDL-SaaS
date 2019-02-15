# coding=utf-8
from django.db import models


class HansReplaceItem(models.Model):
    chn_word=models.CharField(max_length=8)
    replaced_by=models.CharField(max_length=16, blank=True, null=True)


class AsciiReplaceItem(models.Model):
    asc_char=models.CharField(max_length=8)
    replaced_by=models.CharField(max_length=16, blank=True, null=True)


class DiceCode(models.Model):
    sn=models.IntegerField()
    word=models.CharField(max_length=16)