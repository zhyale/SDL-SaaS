# coding=utf-8
from django.db import models
from usermgmt.models import *
from flowmgmt.models import *
from pmp.choice import *

# Project
class Project(models.Model):
    flow = models.ForeignKey(ProjectFlow, blank=True, null=True, related_name='flow_projects')
    team = models.ForeignKey(Team, blank=True, related_name='team_projects')
    product_type=models.CharField(max_length=32, choices=PRODUCT_TYPE_CHOICES, default='GEN')
    phase = models.ForeignKey(ProjectPhase)
    status = models.ForeignKey(ProjectStatus)
    no = models.CharField(max_length=64)
    name = models.CharField(max_length=256)
    objective = models.CharField(max_length=1024, blank=True, null=True)
    introduction = models.CharField(max_length=4096, blank=True, null=True)
    creator = models.ForeignKey(User, blank=True, null=True, related_name='creator_projects')
    manager = models.ForeignKey(User, blank=True, null=True, related_name='manager_projects')
    architect = models.ForeignKey(User, blank=True, null=True, related_name='architect_projects')
    dev_rep = models.ForeignKey(User, blank=True, null=True, related_name='dev_rep_projects')
    test_rep = models.ForeignKey(User, blank=True, null=True, related_name='test_rep_projects')
    security_reviewer = models.ForeignKey(User, blank=True, null=True, related_name='security_reviewer_projects')
    op_rep = models.ForeignKey(User, blank=True, null=True, related_name='op_projects')
    members = models.ManyToManyField(User, blank=True, related_name='member_projects')
    plan_start_date = models.DateField(blank=True, null=True)
    actual_start_date = models.DateField(blank=True, null=True)
    plan_end_date = models.DateField(blank=True, null=True)
    actual_end_date = models.DateField(blank=True, null=True)
    current_handler = models.ForeignKey(User, blank=True, null=True, related_name='current_handler_projects')
    mandays = models.FloatField(default=0.0)
    manday_cost = models.FloatField(default=1000.0)
    currency_unit = models.CharField(max_length=32, default="元")
    # from here used for Full Project Management
    sponsor = models.ForeignKey(User, blank=True, null=True, related_name='sponsor_projects')
    business_rep = models.ForeignKey(User, blank=True, null=True, related_name='business_rep_projects')
    chief_reviewer = models.ForeignKey(User, blank=True, null=True, related_name='reviewer_projects')
    purchasing_rep = models.ForeignKey(User, blank=True, null=True, related_name='purchasing_rep_projects')
    peer_reviewer = models.ForeignKey(User, blank=True, null=True, related_name='peer_reviewer_projects')
    user_rep = models.ForeignKey(User, blank=True, null=True, related_name='user_rep_projects')
    stakeholders = models.ManyToManyField(User, blank=True, related_name='stakeholder_projects')
    qa = models.ForeignKey(User, blank=True, null=True, related_name='qa_projects')  # QA
    qc = models.ForeignKey(User, blank=True, null=True, related_name='qc_projects')  # QC
    hardware_cost = models.FloatField(default=0.0)
    software_cost = models.FloatField(default=0.0)
    other_cost = models.FloatField(default=0.0)
    annual_license_cost = models.FloatField(default=0.0)
    other_annual_cost = models.FloatField(default=0.0)
    # end Full Project Management

    def __unicode__(self):
        return self.name

    def can_be_deleted_by(self, user):
        if user == self.manager:
            return True
        return False

    def get_current_options(self):
        return self.status.status_options.all()


class ProjectApproval(models.Model):
    handle_time = models.DateTimeField(auto_now_add=True)
    handler = models.ForeignKey(User, blank=True, null=True, related_name='project_handler_approvals') # null for system
    project = models.ForeignKey(Project, related_name='project_approvals')
    option = models.ForeignKey(ProjectOption, blank=True, null=True) # null for create
    remarks = models.CharField(max_length=128, blank=True, null=True)
    trustee = models.ForeignKey(User, blank=True, null=True, related_name='project_trustee_approvals')
