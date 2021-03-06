# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-27 11:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usermgmt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usermgmt.Team')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectFlow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('type', models.CharField(choices=[(b'AGL', b'\xe7\xb2\xbe\xe7\xae\x80\xe5\xae\x89\xe5\x85\xa8\xe5\x86\x85\xe6\x8e\xa7\xe9\xa1\xb9\xe7\x9b\xae\xe7\xae\xa1\xe7\x90\x86\xe6\xb5\x81\xe7\xa8\x8b'), (b'APP', b'\xe5\xba\x94\xe7\x94\xa8\xe5\xbc\x80\xe5\x8f\x91\xe5\xae\x89\xe5\x85\xa8\xe5\x86\x85\xe6\x8e\xa7\xe9\xa1\xb9\xe7\x9b\xae\xe7\xae\xa1\xe7\x90\x86\xe6\xb5\x81\xe7\xa8\x8b'), (b'INF', b'\xe5\xa4\x96\xe8\xb4\xad\xe8\xbd\xaf\xe4\xbb\xb6\xe5\x8c\x85\xe5\xae\x9e\xe6\x96\xbd\xe5\xae\x89\xe5\x85\xa8\xe5\x86\x85\xe6\x8e\xa7\xe9\xa1\xb9\xe7\x9b\xae\xe7\xae\xa1\xe7\x90\x86\xe6\xb5\x81\xe7\xa8\x8b'), (b'CUS', b'\xe8\x87\xaa\xe5\xae\x9a\xe4\xb9\x89\xe9\xa1\xb9\xe7\x9b\xae\xe7\xae\xa1\xe7\x90\x86\xe6\xb5\x81\xe7\xa8\x8b')], default=b'CUS', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('do', models.CharField(choices=[(b'SUBMIT', b'\xe6\x8f\x90\xe4\xba\xa4\xe5\xae\xa1\xe6\xa0\xb8'), (b'APPROVE', b'\xe5\x90\x8c\xe6\x84\x8f'), (b'RETURN', b'\xe8\xbf\x94\xe5\x9b\x9e'), (b'TRANSFER', b'\xe8\xbd\xac\xe4\xbb\x96\xe4\xba\xba\xe5\xa4\x84\xe7\x90\x86'), (b'UPDATE', b'\xe5\xa4\x87\xe6\xb3\xa8/\xe6\x9b\xb4\xe6\x96\xb0\xe8\xbf\x9b\xe5\xba\xa6\xe8\xaf\xb4\xe6\x98\x8e')], max_length=32, verbose_name=b'\xe5\x8a\xa8\xe4\xbd\x9c')),
                ('opinion', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectPhase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ready_state', models.CharField(choices=[(b'PLAN', b'\xe8\xa7\x84\xe5\x88\x92\xe4\xb8\xad'), (b'PROCESS', b'\xe8\xbf\x9b\xe8\xa1\x8c\xe4\xb8\xad'), (b'CLOSE', b'\xe5\xb7\xb2\xe7\xbb\x93\xe6\x9d\x9f')], max_length=32)),
                ('sort_no', models.IntegerField()),
                ('flow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flowmgmt.ProjectFlow')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(b'IN_PROCESS', b'\xe8\xbf\x9b\xe8\xa1\x8c\xe4\xb8\xad'), (b'IN_APPROVAL', b'\xe5\xae\xa1\xe6\x89\xb9\xe4\xb8\xad'), (b'IN_OPERATION', b'\xe5\xb7\xb2\xe7\xbb\x93\xe6\x9d\x9f')], max_length=128)),
                ('description', models.CharField(blank=True, max_length=128, null=True)),
                ('handler_role', models.CharField(choices=[(b'PM', b'\xe9\xa1\xb9\xe7\x9b\xae\xe7\xbb\x8f\xe7\x90\x86'), (b'ARCHITECT', b'\xe6\x9e\xb6\xe6\x9e\x84\xe5\xb8\x88/\xe6\x96\xb9\xe6\xa1\x88\xe8\xae\xbe\xe8\xae\xa1\xe5\xb8\x88'), (b'DEV_REP', b'\xe5\xbc\x80\xe5\x8f\x91\xe4\xbb\xa3\xe8\xa1\xa8'), (b'TEST_REP', b'\xe6\xb5\x8b\xe8\xaf\x95\xe4\xbb\xa3\xe8\xa1\xa8'), (b'OP_REP', b'\xe8\xbf\x90\xe7\xbb\xb4\xe4\xbb\xa3\xe8\xa1\xa8'), (b'SECURITY_REVIEWER', b'\xe5\xae\x89\xe5\x85\xa8\xe5\xae\xa1\xe6\xa0\xb8\xe5\x91\x98'), (b'SPONSOR', b'Sponsor(\xe8\xb5\x9e\xe5\x8a\xa9\xe4\xba\xba/\xe4\xba\xba\xe5\x8a\x9b\xe5\x8f\x8a\xe9\xa2\x84\xe7\xae\x97\xe5\x86\xb3\xe7\xad\x96\xe4\xba\xba)'), (b'CHIEF_REVIEWER', b'\xe4\xb8\xbb\xe5\xae\xa1\xe4\xba\xba(\xe6\x8a\x80\xe6\x9c\xaf\xe8\xaf\x84\xe5\xae\xa1\xe7\xbb\x84\xe7\xbb\x84\xe9\x95\xbf)'), (b'PEER_REVIEWER', b'\xe5\x90\x8c\xe8\xa1\x8c\xe8\xaf\x84\xe5\xae\xa1(\xe4\xb8\x93\xe5\xae\xb6\xe4\xbb\xa3\xe8\xa1\xa8)'), (b'BUSINESS_REP', b'\xe4\xb8\x9a\xe5\x8a\xa1\xe4\xbb\xa3\xe8\xa1\xa8(\xe9\x9c\x80\xe6\xb1\x82\xe5\xae\xa1\xe6\xa0\xb8\xe7\xa1\xae\xe8\xae\xa4)'), (b'PURCHASING_REP', b'\xe9\x87\x87\xe8\xb4\xad\xe4\xbb\xa3\xe8\xa1\xa8(\xe6\x8b\x9b\xe6\xa0\x87/\xe9\x80\x89\xe5\x9e\x8b\xe7\xbb\x93\xe6\x9e\x9c\xe7\xa1\xae\xe8\xae\xa4)'), (b'USER_REP', b'\xe7\x94\xa8\xe6\x88\xb7\xe4\xbb\xa3\xe8\xa1\xa8(UAT\xe6\xb5\x8b\xe8\xaf\x95\xe7\xbb\x93\xe6\x9e\x9c\xe7\xa1\xae\xe8\xae\xa4)'), (b'QA', b'QA\xe8\xb4\xa8\xe9\x87\x8f\xe4\xbf\x9d\xe9\x9a\x9c'), (b'QC', b'QC\xe8\xb4\xa8\xe9\x87\x8f\xe6\x8e\xa7\xe5\x88\xb6'), (b'TASK_LEADER', b'\xe4\xbb\xbb\xe5\x8a\xa1\xe8\xb4\x9f\xe8\xb4\xa3\xe4\xba\xba'), (b'TASK_REVIEWER', b'\xe4\xbb\xbb\xe5\x8a\xa1\xe5\xa4\x8d\xe6\xa0\xb8\xe4\xba\xba'), (b'NONE', b'\xe4\xb8\x8d\xe9\x9c\x80\xe8\xa6\x81\xe5\xa4\x84\xe7\x90\x86')], max_length=64)),
                ('phase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phase_statuses', to='flowmgmt.ProjectPhase')),
            ],
        ),
        migrations.CreateModel(
            name='TaskFlow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('type', models.CharField(choices=[(b'GEN', b'\xe9\x80\x9a\xe7\x94\xa8\xe5\xb7\xa5\xe4\xbd\x9c\xe6\xb5\x81'), (b'SEC_DESIGN', b'\xe5\xae\x89\xe5\x85\xa8\xe8\xae\xbe\xe8\xae\xa1\xe8\x87\xaa\xe6\xa3\x80\xe5\xb7\xa5\xe4\xbd\x9c\xe6\xb5\x81'), (b'SEC_DEV', b'\xe5\xae\x89\xe5\x85\xa8\xe5\xbc\x80\xe5\x8f\x91\xe8\x87\xaa\xe6\xa3\x80\xe5\xb7\xa5\xe4\xbd\x9c\xe6\xb5\x81'), (b'SEC_TEST', b'\xe5\xae\x89\xe5\x85\xa8\xe6\xb5\x8b\xe8\xaf\x95\xe8\x87\xaa\xe6\xa3\x80\xe5\xb7\xa5\xe4\xbd\x9c\xe6\xb5\x81'), (b'SEC_DEPLOY', b'\xe5\xae\x89\xe5\x85\xa8\xe9\x83\xa8\xe7\xbd\xb2\xe8\x87\xaa\xe6\xa3\x80\xe5\xb7\xa5\xe4\xbd\x9c\xe6\xb5\x81'), (b'ACCEPT', b'\xe9\xaa\x8c\xe6\x94\xb6\xe5\xb7\xa5\xe4\xbd\x9c\xe6\xb5\x81'), (b'REQ_CONFIRM', b'\xe9\x9c\x80\xe6\xb1\x82\xe7\xa1\xae\xe8\xae\xa4\xe5\xb7\xa5\xe4\xbd\x9c\xe6\xb5\x81'), (b'BID', b'\xe9\x80\x89\xe5\x9e\x8b\xe5\xb7\xa5\xe4\xbd\x9c\xe6\xb5\x81'), (b'DESIGN_TR', b'\xe6\x96\xb9\xe6\xa1\x88\xe8\xae\xbe\xe8\xae\xa1\xe8\xaf\x84\xe5\xae\xa1\xe8\x87\xaa\xe6\xa3\x80\xe5\xb7\xa5\xe4\xbd\x9c\xe6\xb5\x81'), (b'PUBLISH_TR', b'\xe4\xb8\x8a\xe7\xba\xbf\xe5\x8f\x91\xe5\xb8\x83\xe8\xaf\x84\xe5\xae\xa1\xe8\x87\xaa\xe6\xa3\x80\xe5\xb7\xa5\xe4\xbd\x9c\xe6\xb5\x81'), (b'SEC_TEST', b'\xe5\xae\x89\xe5\x85\xa8\xe6\xb5\x8b\xe8\xaf\x95\xe5\xb7\xa5\xe4\xbd\x9c\xe6\xb5\x81'), (b'SEC_CFG', b'\xe5\xae\x89\xe5\x85\xa8\xe9\x85\x8d\xe7\xbd\xae\xe5\xb7\xa5\xe4\xbd\x9c\xe6\xb5\x81'), (b'BACKUP', b'\xe5\xa4\x87\xe4\xbb\xbd\xe5\xb7\xa5\xe4\xbd\x9c\xe6\xb5\x81'), (b'CUS', b'\xe8\x87\xaa\xe5\xae\x9a\xe4\xb9\x89\xe5\xb7\xa5\xe4\xbd\x9c\xe6\xb5\x81'), (b'TEAMWORK', b'\xe5\x8d\x8f\xe4\xbd\x9c\xe5\xb7\xa5\xe4\xbd\x9c\xe6\xb5\x81')], default=b'CUS', max_length=128)),
                ('description', models.TextField(blank=True, max_length=2048, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('do', models.CharField(choices=[(b'SUBMIT', b'\xe6\x8f\x90\xe4\xba\xa4\xe5\xae\xa1\xe6\xa0\xb8'), (b'APPROVE', b'\xe5\x90\x8c\xe6\x84\x8f'), (b'RETURN', b'\xe8\xbf\x94\xe5\x9b\x9e'), (b'TRANSFER', b'\xe8\xbd\xac\xe4\xbb\x96\xe4\xba\xba\xe5\xa4\x84\xe7\x90\x86'), (b'UPDATE', b'\xe5\xa4\x87\xe6\xb3\xa8/\xe6\x9b\xb4\xe6\x96\xb0\xe8\xbf\x9b\xe5\xba\xa6\xe8\xaf\xb4\xe6\x98\x8e')], max_length=32, verbose_name=b'\xe5\x8a\xa8\xe4\xbd\x9c')),
                ('opinion', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=128)),
                ('handler_role', models.CharField(choices=[(b'PM', b'\xe9\xa1\xb9\xe7\x9b\xae\xe7\xbb\x8f\xe7\x90\x86'), (b'ARCHITECT', b'\xe6\x9e\xb6\xe6\x9e\x84\xe5\xb8\x88/\xe6\x96\xb9\xe6\xa1\x88\xe8\xae\xbe\xe8\xae\xa1\xe5\xb8\x88'), (b'DEV_REP', b'\xe5\xbc\x80\xe5\x8f\x91\xe4\xbb\xa3\xe8\xa1\xa8'), (b'TEST_REP', b'\xe6\xb5\x8b\xe8\xaf\x95\xe4\xbb\xa3\xe8\xa1\xa8'), (b'OP_REP', b'\xe8\xbf\x90\xe7\xbb\xb4\xe4\xbb\xa3\xe8\xa1\xa8'), (b'SECURITY_REVIEWER', b'\xe5\xae\x89\xe5\x85\xa8\xe5\xae\xa1\xe6\xa0\xb8\xe5\x91\x98'), (b'SPONSOR', b'Sponsor(\xe8\xb5\x9e\xe5\x8a\xa9\xe4\xba\xba/\xe4\xba\xba\xe5\x8a\x9b\xe5\x8f\x8a\xe9\xa2\x84\xe7\xae\x97\xe5\x86\xb3\xe7\xad\x96\xe4\xba\xba)'), (b'CHIEF_REVIEWER', b'\xe4\xb8\xbb\xe5\xae\xa1\xe4\xba\xba(\xe6\x8a\x80\xe6\x9c\xaf\xe8\xaf\x84\xe5\xae\xa1\xe7\xbb\x84\xe7\xbb\x84\xe9\x95\xbf)'), (b'PEER_REVIEWER', b'\xe5\x90\x8c\xe8\xa1\x8c\xe8\xaf\x84\xe5\xae\xa1(\xe4\xb8\x93\xe5\xae\xb6\xe4\xbb\xa3\xe8\xa1\xa8)'), (b'BUSINESS_REP', b'\xe4\xb8\x9a\xe5\x8a\xa1\xe4\xbb\xa3\xe8\xa1\xa8(\xe9\x9c\x80\xe6\xb1\x82\xe5\xae\xa1\xe6\xa0\xb8\xe7\xa1\xae\xe8\xae\xa4)'), (b'PURCHASING_REP', b'\xe9\x87\x87\xe8\xb4\xad\xe4\xbb\xa3\xe8\xa1\xa8(\xe6\x8b\x9b\xe6\xa0\x87/\xe9\x80\x89\xe5\x9e\x8b\xe7\xbb\x93\xe6\x9e\x9c\xe7\xa1\xae\xe8\xae\xa4)'), (b'USER_REP', b'\xe7\x94\xa8\xe6\x88\xb7\xe4\xbb\xa3\xe8\xa1\xa8(UAT\xe6\xb5\x8b\xe8\xaf\x95\xe7\xbb\x93\xe6\x9e\x9c\xe7\xa1\xae\xe8\xae\xa4)'), (b'QA', b'QA\xe8\xb4\xa8\xe9\x87\x8f\xe4\xbf\x9d\xe9\x9a\x9c'), (b'QC', b'QC\xe8\xb4\xa8\xe9\x87\x8f\xe6\x8e\xa7\xe5\x88\xb6'), (b'TASK_LEADER', b'\xe4\xbb\xbb\xe5\x8a\xa1\xe8\xb4\x9f\xe8\xb4\xa3\xe4\xba\xba'), (b'TASK_REVIEWER', b'\xe4\xbb\xbb\xe5\x8a\xa1\xe5\xa4\x8d\xe6\xa0\xb8\xe4\xba\xba'), (b'NONE', b'\xe4\xb8\x8d\xe9\x9c\x80\xe8\xa6\x81\xe5\xa4\x84\xe7\x90\x86')], max_length=64)),
                ('sort_no', models.IntegerField()),
                ('ready_state', models.CharField(choices=[(b'TODO', b'\xe5\xbe\x85\xe6\x89\xa7\xe8\xa1\x8c'), (b'PROCESSING', b'\xe6\x89\xa7\xe8\xa1\x8c\xe4\xb8\xad'), (b'REVIEW', b'\xe5\xa4\x8d\xe6\xa0\xb8\xe4\xb8\xad'), (b'DONE', b'\xe5\xb7\xb2\xe5\xae\x8c\xe6\x88\x90')], max_length=32)),
                ('flow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flow_statuses', to='flowmgmt.TaskFlow')),
                ('next_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nextstatus_statuses', to='flowmgmt.TaskStatus')),
                ('pre_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prestatus_statuses', to='flowmgmt.TaskStatus')),
            ],
        ),
        migrations.AddField(
            model_name='taskoption',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_options', to='flowmgmt.TaskStatus'),
        ),
        migrations.AddField(
            model_name='taskflow',
            name='first_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='flowmgmt.TaskStatus'),
        ),
        migrations.AddField(
            model_name='taskflow',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_task_flows', to='usermgmt.Team'),
        ),
        migrations.AddField(
            model_name='projectphase',
            name='kcp_flows',
            field=models.ManyToManyField(blank=True, related_name='kcp_phases', to='flowmgmt.TaskFlow'),
        ),
        migrations.AddField(
            model_name='projectphase',
            name='next_phase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='flowmgmt.ProjectPhase'),
        ),
        migrations.AddField(
            model_name='projectphase',
            name='phase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flowmgmt.Phase'),
        ),
        migrations.AddField(
            model_name='projectoption',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_options', to='flowmgmt.ProjectStatus'),
        ),
        migrations.AddField(
            model_name='projectflow',
            name='first_phase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='flowmgmt.ProjectPhase'),
        ),
        migrations.AddField(
            model_name='projectflow',
            name='phases',
            field=models.ManyToManyField(through='flowmgmt.ProjectPhase', to='flowmgmt.Phase'),
        ),
        migrations.AddField(
            model_name='projectflow',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_flows', to='usermgmt.Team'),
        ),
    ]
