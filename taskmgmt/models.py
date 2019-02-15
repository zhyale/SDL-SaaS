# coding=utf-8
from django.db import models
from usermgmt.models import *
from projectmgmt.models import Project
from flowmgmt.models import ProjectPhase, TaskFlow, TaskStatus, TaskOption
from pmp.choice import PRODUCT_TYPE_CHOICES, CHECK_RESULT_CHOICES, CUSTOM_CHECK_RESULT_CHOICES


class CheckItem(models.Model):
    description = models.CharField(max_length=512)
    flow = models.ForeignKey(TaskFlow, blank=True, null=True, related_name='flow_check_items')
    sort_no = models.IntegerField()
    product_type=models.CharField(max_length=32, choices=PRODUCT_TYPE_CHOICES)

    def __unicode__(self):
        return '[' + self.flow.name + '][' +self.product_type + ']' + self.description


class Task(models.Model):
    assign_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=2048, blank=True, null=True)
    deliverable_url = models.CharField(max_length=1024, blank=True, null=True, default='')
    assigner = models.ForeignKey(User, blank=True, null=True, related_name='assigner_tasks')  # null for system task
    leader = models.ForeignKey(User, related_name='leader_tasks')
    members = models.ManyToManyField(User, blank=True, related_name='member_tasks')
    reviewer = models.ForeignKey(User, related_name='reviewer_tasks')
    current_handler = models.ForeignKey(User, blank=True, null=True, related_name='current_handler_tasks')
    plan_mandays = models.FloatField(default=1.0)
    actual_mandays = models.FloatField(blank=True, null=True, default=0.0)
    project = models.ForeignKey(Project, related_name='project_tasks', blank=True, null=True)
    is_kcp = models.BooleanField(default=False)
    is_subtask = models.BooleanField(default=False)
    parent_task = models.ForeignKey('self', blank=True, null=True, related_name='subtasks')
    done_in_project_phase = models.ForeignKey(ProjectPhase, blank=True, null=True, related_name='phase_tasks')
    deadline = models.DateTimeField(blank=True, null=True)
    done_time = models.DateTimeField(blank=True, null=True)
    flow = models.ForeignKey(TaskFlow, related_name='flow_tasks')
    status = models.ForeignKey(TaskStatus, related_name='status_tasks')
    team = models.ForeignKey(Team, blank=True, null=True, related_name='team_tasks')
    checklist = models.ManyToManyField(CheckItem, through='CheckResult')

    def __unicode__(self):
        if self.project:
            return '['+ self.project.name + ']'+self.name
        return self.name

    def can_be_deleted_by(self, user):
        if user == self.assigner:
            return True
        project = self.project
        if project:
            if user == project.manager:
                return True
        return False


class TaskApproval(models.Model):
    handle_time = models.DateTimeField(auto_now_add=True)
    handler = models.ForeignKey(User, blank=True, null=True, related_name='task_handler_approvals')
    task = models.ForeignKey(Task, related_name='task_approvals')
    option = models.ForeignKey(TaskOption, blank=True, null=True)  # null for create
    remarks = models.CharField(max_length=128, blank=True, null=True)
    trustee = models.ForeignKey(User, blank=True, null=True, related_name='task_trustee_approvals')


class CheckResult(models.Model):
    task = models.ForeignKey(Task, related_name='task_checkresults')
    check_item = models.ForeignKey(CheckItem)
    result = models.CharField(max_length=16, blank=True, null=True, choices=CHECK_RESULT_CHOICES, default='NONE')


class CustomCheckResult(models.Model):
    task = models.ForeignKey(Task, related_name='custom_checkresults')
    check_item = models.CharField(max_length=256)
    result = models.CharField(max_length=16, choices=CUSTOM_CHECK_RESULT_CHOICES, default='NONE')
