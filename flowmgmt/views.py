# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from models import *
from usermgmt.utils import get_valid_user, init_demo_users
from utils import  init_flows
from taskmgmt.utils import init_checklist
from flowmgmt.utils import task_flow_json
from wikimgmt.utils import init_wiki_items
from pagemgmt.utils import init_pages
from itsm.utils import init_demo_cis
from pmp.cache import get_project_flow_by_id, get_project_flow_json_by_id, get_task_flow_by_id, get_task_flow_json_by_id
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


# Project
def ProjectFlowInfo(request, fid):
    _user = get_valid_user(request)
    if _user:
        _fid = int(fid)
        try:
            _flow = get_project_flow_by_id(_fid)
            _flow_json=get_project_flow_json_by_id(_fid)
            _projects = _flow.flow_projects.filter(team__in=_user.member_teams.all())
            if request.method == "GET":
                return render(request, 'projectflowinfo.html',
                              {'current_user': _user, 'flow': _flow, 'flow_json':_flow_json, 'projects': _projects, })
        except:
            messages.add_message(request, messages.INFO, '您查询的流程不存在！')
            return render(request, 'index.html', {'current_user': _user})
    return HttpResponseRedirect('/login')


def FlowDelete(request):
    _user = get_valid_user(request)
    if _user:
        _fid = request.POST.get("fid", "")
        if _fid:
            _type = request.POST.get("type", "")
            if _type == 'project':
                _flow = ProjectFlow.objects.get(id=_fid)
                if _user in _flow.team.admins.all():
                    _projects = _flow.flow_projects.all()
                    if len(_projects) == 0:
                        _flow.delete()
            elif _type == 'task':
                _flow = TaskFlow.objects.get(id=_fid)
                if _user in _flow.team.admins.all():
                    _tasks = _flow.flow_tasks.all()
                    if len(_tasks) == 0:
                        _flow.delete()
            return HttpResponseRedirect('/flowlist')
    return HttpResponseRedirect('/login')


def show_flow_list(request):
    return show_flow_list_and_flow(request, None, None)


def show_flow_list_and_flow(request, flow_cat, fid):
    _user = get_valid_user(request)
    if _user:
        if request.method == "GET":
            _default_project_flows = ProjectFlow.objects.exclude(type='CUS')
            _default_task_flows = TaskFlow.objects.exclude(type="CUS")
            _teams = _user.member_teams.all()
            _cus_project_flows = ProjectFlow.objects.filter(team__in=_teams)
            _cus_task_flows = TaskFlow.objects.filter(team__in=_teams)
            return render(request, 'flowlist.html', {'current_user': _user, 'teams': _teams,
                                                     'default_project_flows': _default_project_flows,
                                                     'default_task_flows': _default_task_flows,
                                                     'cus_project_flows': _cus_project_flows,
                                                     'cus_task_flows': _cus_task_flows,
                                                     'flow_cat':flow_cat,
                                                     'fid':fid})
    return HttpResponseRedirect('/login')


def TaskFlowInfo(request, fid):
    _user = get_valid_user(request)
    if _user:
        _fid = int(fid)
        try:
            _flow = get_task_flow_by_id(_fid)
            _flow_json=get_task_flow_json_by_id(_fid)
            _tasks = _flow.flow_tasks.filter(team__in=_user.member_teams.all())
            if request.method == "GET":
                return render(request, 'taskflowinfo.html', {'current_user': _user, 'flow': _flow,'flow_json':_flow_json, 'tasks': _tasks})
        except:
            messages.add_message(request, messages.INFO, '您查询的流程不存在！')
            return render(request, 'index.html', {'current_user': _user})
    return HttpResponseRedirect('/login')


def init_system(request):
    init_flows()
    init_checklist()
    init_demo_users()
    init_wiki_items()
    init_pages()
    init_demo_cis()
    return HttpResponse('OK')