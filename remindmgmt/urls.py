# coding=utf-8
from django.conf.urls import patterns, url
import remindmgmt.views

urlpatterns = [
    url(r'^create/([a-z]+)', remindmgmt.views.create_remind),
    url(r'^finish/(\d+)', remindmgmt.views.mark_remind_finish),
    url(r'^undo/(\d+)', remindmgmt.views.mark_remind_unfinish),
]
