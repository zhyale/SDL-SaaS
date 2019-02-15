# coding=utf-8
from django.conf.urls import patterns, url
import toolmgmt.views

urlpatterns = [
    url(r'^ip$', toolmgmt.views.ip_address_portal),
    url(r'^ip/([\d\.]+)$', toolmgmt.views.ip_address),
    url(r'^ip/initipsegment$', toolmgmt.views.init_ip_segment),
]
