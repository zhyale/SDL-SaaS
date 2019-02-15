# coding=utf-8
from django.conf.urls import patterns, url
import pwdmgmt.views

urlpatterns = [
    url(r'^generator$', pwdmgmt.views.password_generation),
]
