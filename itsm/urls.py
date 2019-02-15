# coding=utf-8
from django.conf.urls import patterns, url
import itsm.views

urlpatterns = [
    url(r'^$', itsm.views.itsm),
    url(r'^configuration-management$', itsm.views.configuration_management),
    url(r'^ci/(\d+)$', itsm.views.show_ci),
    url(r'^ci/([a-z]+)$', itsm.views.ci_operation),
    url(r'^ip-management$', itsm.views.ip_management),
    url(r'^ip/(\d+)$', itsm.views.show_ip),
    url(r'^domain-management$', itsm.views.domain_management),
    url(r'^domain/(\d+)$', itsm.views.show_domain),
    url(r'^change-management$', itsm.views.change_management),
    url(r'^event-management$', itsm.views.event_management),
    url(r'^problem-management$', itsm.views.problem_management),
]
