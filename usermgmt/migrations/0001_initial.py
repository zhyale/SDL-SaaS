# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-27 11:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('top_domain_name', models.CharField(max_length=128, unique=True)),
                ('abbr', models.CharField(blank=True, max_length=32, null=True)),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DayStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('pv', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('abbr', models.CharField(max_length=32)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('vip_expire_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('salt', models.CharField(default=b'eUAmmjNo', max_length=8)),
                ('hashpwd', models.CharField(default=b'0cf521620fff49efec6774413ac4d0aa3b389a9526b9d5604cf204d998b5c6307446ebd417c5234d5b52de4d8bf21ab3fe51268b70930db5411a67a2b858d657', max_length=128)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('email_checked', models.BooleanField(default=True)),
                ('check_code', models.CharField(blank=True, max_length=8, null=True)),
                ('nickname', models.CharField(blank=True, default=b'\xe5\x8c\xbf\xe5\x90\x8d', max_length=64, null=True)),
                ('mobile', models.CharField(blank=True, max_length=32, null=True)),
                ('location', models.CharField(blank=True, max_length=512, null=True)),
                ('department', models.CharField(blank=True, max_length=512, null=True)),
                ('introduction', models.CharField(blank=True, max_length=1024, null=True)),
                ('last_login_time', models.DateTimeField(auto_now=True, null=True)),
                ('last_login_ip', models.CharField(blank=True, max_length=128, null=True)),
                ('avatar_link', models.CharField(blank=True, max_length=512, null=True)),
                ('need_modify_pwd', models.BooleanField(default=False)),
                ('career_tags', models.ManyToManyField(blank=True, related_name='tag_users', to='usermgmt.Tag')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_users', to='usermgmt.Company')),
                ('default_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='default_team_users', to='usermgmt.Team')),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='admins',
            field=models.ManyToManyField(blank=True, related_name='admin_teams', to='usermgmt.User'),
        ),
        migrations.AddField(
            model_name='team',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_teams', to='usermgmt.Company'),
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='member_teams', to='usermgmt.User'),
        ),
        migrations.AddField(
            model_name='daystat',
            name='visitors',
            field=models.ManyToManyField(blank=True, to='usermgmt.User'),
        ),
    ]