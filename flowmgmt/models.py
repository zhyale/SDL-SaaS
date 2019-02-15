# coding=utf-8
from django.db import models
from usermgmt.models import Team
from pmp.choice import *
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Phase(models.Model):
    name = models.CharField(max_length=128, unique=True)
    team = models.ForeignKey(Team, blank=True, null=True)  # None for default

    def __unicode__(self):
        return self.name


class ProjectFlow(models.Model):
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128, choices=PROJECT_FLOW_TYPE_CHOICES, default='CUS')
    phases = models.ManyToManyField(Phase, through='ProjectPhase')
    first_phase = models.ForeignKey('ProjectPhase', blank=True, null=True)
    team = models.ForeignKey(Team, blank=True, null=True, related_name="team_flows")

    def __unicode__(self):
        return self.name


class ProjectPhase(models.Model):
    ready_state = models.CharField(max_length=32, choices=PROJECT_PHASE_READY_STATES)
    flow = models.ForeignKey(ProjectFlow)
    phase = models.ForeignKey(Phase)
    sort_no = models.IntegerField()
    next_phase = models.ForeignKey('self', blank=True, null=True)
    kcp_flows = models.ManyToManyField('TaskFlow', blank=True, related_name='kcp_phases')

    def __unicode__(self):
        return '[' + self.flow.name + '][' + self.phase.name + ']'


class ProjectStatus(models.Model):
    phase = models.ForeignKey(ProjectPhase, related_name='phase_statuses')
    status = models.CharField(max_length=128, choices=PROJECT_STATUS_CHOICES)
    description = models.CharField(max_length=128, blank=True, null=True)
    handler_role = models.CharField(max_length=64, choices=ROLE_CHOICES)

    def __unicode__(self):
        return '[' + self.phase.flow.name + '][' + self.phase.phase.name + '][' + self.get_status_display() + "]"


class ProjectOption(models.Model):
    status = models.ForeignKey(ProjectStatus, related_name='status_options')
    do = models.CharField(max_length=32, choices=FLOW_APPROVAL_CHOICES, verbose_name='动作')
    opinion = models.CharField(max_length=128)

    def __unicode__(self):
        return self.opinion


class TaskFlow(models.Model):
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128, choices=TASK_FLOW_TYPE_CHOICES, default='CUS')
    description = models.TextField(max_length=2048, blank=True, null=True)
    team = models.ForeignKey(Team, blank=True, null=True, related_name="team_task_flows")
    first_status=models.ForeignKey('TaskStatus', blank=True, null=True)

    def __unicode__(self):
        return self.name

    def current_status_dict(self, current_status):
        flow_list = json.loads(self.flow_json, encoding="utf-8")
        for status_dict in flow_list:
            if status_dict["status"] == current_status:
                return status_dict
        return {}


class TaskStatus(models.Model):
    name=models.CharField(max_length=128)
    description=models.CharField(max_length=128)
    flow=models.ForeignKey(TaskFlow, related_name='flow_statuses')
    handler_role=models.CharField(max_length=64, choices=ROLE_CHOICES)
    sort_no = models.IntegerField()
    pre_status = models.ForeignKey('self', blank=True, null=True, related_name='prestatus_statuses')
    next_status = models.ForeignKey('self', blank=True, null=True, related_name='nextstatus_statuses')
    ready_state=models.CharField(max_length=32, choices=TASK_READY_STATES)

    def __unicode__(self):
        return '[' + self.flow.name + '][' + self.name + ']'


class TaskOption(models.Model):
    status = models.ForeignKey(TaskStatus, related_name='status_options')
    do = models.CharField(max_length=32, choices=FLOW_APPROVAL_CHOICES, verbose_name='动作')
    opinion = models.CharField(max_length=128)

    def __unicode__(self):
        return self.opinion