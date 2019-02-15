# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.contrib import messages
import pmp.settings
from usermgmt.utils import get_valid_user
from msgmgmt.utils import send_circle_msg
from models import *
from utils import handle_project_approval, has_view_privileges_for_project
from taskmgmt.utils import create_kcp_tasks
import datetime
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')


def ProjectInfo(request, pid):
    _user = get_valid_user(request)
    if _user:
        _id = int(pid)  # request.GET.get("id")
        try:
            _project = Project.objects.get(id=_id)
        except:
            return render(request, 'projectinfo.html', {'current_user': _user, 'project': None, 'exp_message':'指定的项目不存在！' })
        # Check privileges, team members or current_handler can view it
        has_privileges = has_view_privileges_for_project(_project, _user)
        if not has_privileges:
            return render(request, 'projectinfo.html', {'current_user': _user, 'project': None, 'exp_message':'您没有查看此项目的权限!'})
        _budget = _project.mandays * _project.manday_cost + _project.hardware_cost + _project.software_cost + _project.other_cost
        _open_kcp_tasks = _project.project_tasks.filter(is_kcp=True, done_in_project_phase=_project.phase).exclude(
            status__ready_state='DONE')
        _all_kcp_tasks = _project.project_tasks.filter(is_kcp=True)
        _project_actual_mandays = _project.project_tasks.filter(status__ready_state='DONE').aggregate(
            Sum('actual_mandays'))
        if not _project_actual_mandays["actual_mandays__sum"]:
            _project_actual_mandays["actual_mandays__sum"] = 0
        _can_be_deleted = _project.can_be_deleted_by(_user)
        return render(request, 'projectinfo.html', {'current_user': _user, 'project': _project,
                                                    'budget': _budget,
                                                    'all_kcp_tasks': _all_kcp_tasks,
                                                    'open_kcp_tasks': _open_kcp_tasks,
                                                    'project_actual_mandays': _project_actual_mandays,
                                                    'can_be_deleted': _can_be_deleted})
    return HttpResponseRedirect('/login')


def ProjectDelete(request):
    _user = get_valid_user(request)
    if _user:
        _pid = request.POST.get("pid", "")
        if _pid:
            _project = Project.objects.get(id=_pid)
            if _project.can_be_deleted_by(_user):
                _project.delete()
        return HttpResponseRedirect('projectlist')
    return HttpResponseRedirect('/login')


def ProjectEdit(request, pid):
    _user = get_valid_user(request)
    if _user:
        _id = int(pid)
        try:
            _project = Project.objects.get(id=_id)
        except:
            messages.add_message(request, messages.INFO, '指定的项目不存在！')
            return render(request, 'index.html', {'current_user': _user})
        if request.method == 'GET':
            return render(request, 'projectedit.html', {'current_user': _user, 'project': _project})
        _project.no = request.POST.get("no", "")
        _project.name = request.POST.get("name", "")
        _project.manager = User.objects.get(id=request.POST.get("manager_id"))
        _project.security_rep = User.objects.get(id=request.POST.get("security_rep_id"))
        _project.op_rep = User.objects.get(id=request.POST.get("op_rep_id"))
        _project.objective = request.POST.get("objective")
        _project.introduction = request.POST.get("introduction")
        _project.sponsor = User.objects.get(id=request.POST.get("sponsor_id"))
        _project.business_rep = User.objects.get(id=request.POST.get("business_rep_id"))
        _project.chief_reviewer = User.objects.get(id=request.POST.get("chief_reviewer_id"))
        _project.peer_reviewer = User.objects.get(id=request.POST.get("peer_reviewer_id"))
        _project.purchasing_rep = User.objects.get(id=request.POST.get("purchasing_rep_id"))
        _project.user_rep = User.objects.get(id=request.POST.get("user_rep_id"))
        _project.qa = User.objects.get(id=request.POST.get("qa_id"))
        _project.qc = User.objects.get(id=request.POST.get("qc_id"))
        _project.plan_start_date = datetime.datetime.strptime(request.POST.get("plan_start_date"), '%Y-%m-%d')
        _project.plan_end_date = datetime.datetime.strptime(request.POST.get("plan_end_date"), '%Y-%m-%d')
        _project.mandays = request.POST.get("mandays")
        _project.manday_cost = request.POST.get("manday_cost")
        _project.currency_unit = request.POST.get("currency_unit")
        _project.hardware_cost = request.POST.get("hardware_cost")
        _project.software_cost = request.POST.get("software_cost")
        _project.other_cost = request.POST.get("other_cost")
        _project.annual_license_cost = request.POST.get("annual_license_cost")
        _project.other_annual_cost = request.POST.get("other_annual_cost")
        # project members
        _members = request.POST.getlist("members", [])
        _project.members.clear()
        for member_id in _members:
            if member_id:
                _member = User.objects.get(id=member_id)
                _project.members.add(_member)
        # project stakeholders
        _stakeholders = request.POST.getlist("stakeholders")
        _project.stakeholders.clear()
        for stakeholder_id in _stakeholders:
            if stakeholder_id:
                _stakeholder = User.objects.get(id=stakeholder_id)
                _project.stakeholders.add(_stakeholder)
        _project.save()
        # create log
        _logtime = datetime.datetime.now()
        _action = 'edit'
        _project_url = pmp.settings.SAAS_PORTAL + '/projectlist/' + str(_project.id)
        _msg = "[" + _logtime.strftime(
            "%Y-%m-%d %H:%M:%S") + "] " + "我修改了项目【" + _project.no + "】" + _project.name + " " + _project_url
        send_circle_msg(_user, _msg)
        ProjectApproval.objects.create(handler=_user, project=_project, remarks='编辑项目')
        return HttpResponseRedirect('/projectlist/' + str(_project.id))
    return HttpResponseRedirect('/login')


def ProjectCreate(request):
    _user = get_valid_user(request)
    if _user:
        _team = _user.get_default_team()
        if request.method == "GET":
            if not _team:
                messages.add_message(request, messages.INFO, '您目前不属于任何团队，请先创建团队或加入现有团队！')
                return render(request, 'teamlist.html', {'current_user': _user})
        _step = request.POST.get("nextstep", "1")
        if _step == "1":
            _agl_flow_id = ProjectFlow.objects.get(type="AGL").id
            _app_flow_id = ProjectFlow.objects.get(type="APP").id
            _inf_flow_id = ProjectFlow.objects.get(type="INF").id
            _flow_id_dict = {'AGL': _agl_flow_id, 'APP': _app_flow_id, 'INF': _inf_flow_id}
            _cus_flows = _team.team_flows.all()
            return render(request, 'pcreate_1.html', {'current_user': _user, 'team': _team, 'cus_flows': _cus_flows,
                                                      'flow_id_dict': _flow_id_dict})
        elif _step == "2":
            _default_project_no = '%03d' % (_team.team_projects.count() + 1)
            _flow_id = int(request.POST.get("fid", ""))
            _flow = ProjectFlow.objects.get(id=_flow_id)
            _curdate = datetime.date.today().strftime("%Y-%m-%d")
            _default_end_date = (datetime.date.today() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
            return render(request, 'pcreate_2.html', {'current_user': _user, 'project_flow': _flow, 'team': _team,
                                                      'default_project_no': _default_project_no, 'curdate': _curdate,
                                                      'default_end_date': _default_end_date})
        elif _step == "3":
            _flow_id = int(request.POST.get("fid", ""))
            _flow = ProjectFlow.objects.get(id=_flow_id)
            _product_type = request.POST.get("product_type", "GEN")
            _tid = request.POST.get("tid", "")
            _team = Team.objects.get(id=_tid)
            _manager_id = request.POST.get("manager_id", "")
            _manager = User.objects.get(id=_manager_id)
            _architect_id = request.POST.get("architect_id", "")
            _architect = User.objects.get(id=_architect_id)
            _dev_rep_id = request.POST.get("dev_rep_id", "")
            _dev_rep = User.objects.get(id=_dev_rep_id)
            _test_rep_id = request.POST.get("test_rep_id", "")
            _test_rep = User.objects.get(id=_test_rep_id)
            _security_reviewer_id = request.POST.get("security_reviewer_id", _manager_id)
            _security_reviewer = User.objects.get(id=_security_reviewer_id)
            _op_rep_id = request.POST.get("op_rep_id", _manager_id)
            _op_rep = User.objects.get(id=_op_rep_id)
            _qa_id = request.POST.get("qa_id", _manager_id)
            _qa = User.objects.get(id=_qa_id)
            _no = request.POST.get("no", "")
            _name = request.POST.get("name", "")
            _objective = request.POST.get("objective")
            _introduction = request.POST.get("introduction")
            _plan_start_date = datetime.datetime.strptime(request.POST.get("plan_start_date"), '%Y-%m-%d')
            _plan_end_date = datetime.datetime.strptime(request.POST.get("plan_end_date"), '%Y-%m-%d')
            _mandays = request.POST.get("mandays")
            _manday_cost = request.POST.get("manday_cost")
            _currency_unit = request.POST.get("currency_unit")
            _phase = _flow.first_phase
            isCreateProject = True
            if pmp.settings.DEBUG:
                try:
                    _project = Project.objects.get(no=_no)
                    isCreateProject = False
                except:
                    pass
            if isCreateProject:
                _project = Project.objects.create(no=_no, name=_name, flow=_flow, team=_team,
                                                  product_type=_product_type,
                                                  creator=_user,
                                                  manager=_manager,
                                                  architect=_architect,
                                                  dev_rep=_dev_rep,
                                                  test_rep=_test_rep,
                                                  security_reviewer=_security_reviewer,
                                                  op_rep=_op_rep,
                                                  sponsor=_manager,
                                                  business_rep=_manager,
                                                  chief_reviewer=_manager,
                                                  purchasing_rep=_manager,
                                                  peer_reviewer=_manager,
                                                  user_rep=_manager,
                                                  qa=_qa,
                                                  qc=_manager,
                                                  objective=_objective, introduction=_introduction,
                                                  plan_start_date=_plan_start_date, plan_end_date=_plan_end_date,
                                                  actual_start_date=_plan_start_date,
                                                  mandays=_mandays, manday_cost=_manday_cost,
                                                  currency_unit=_currency_unit,
                                                  current_handler=_manager,
                                                  phase=_phase,
                                                  status=_phase.phase_statuses.get(status='IN_PROCESS'))
                ProjectApproval.objects.create(handler=_user, project=_project, remarks='创建了项目')
                # Create KCP Task for AGL
                if _flow.type == "AGL":
                    create_kcp_tasks(_project)
            _member_ids = request.POST.getlist("members", [])
            for _memberid in _member_ids:
                if _memberid:
                    _member = User.objects.get(id=_memberid)
                    _project.members.add(_member)
                    _project.team.members.add(_member)
            _project.save()
            _project.team.save()
            if _flow.type == "AGL":
                messages.add_message(request, messages.INFO, '项目创建成功！')
                _msg = '我创建了项目【%s】%s %s' % (
                    _project.no, _project.name, pmp.settings.SAAS_PORTAL + '/projectlist/' + str(_project.id))
                send_circle_msg(_user, _msg)
                return HttpResponseRedirect('/projectlist/' + str(_project.id))
            else:
                messages.add_message(request, messages.INFO, '根据您选择的项目管理流程类型，请继续补充完善如下信息：')
                return render(request, 'pcreate_3.html',
                              {'current_user': _user, 'project': _project})
        elif _step == "4":
            _project = Project.objects.get(id=request.POST.get("pid"))
            _sponsor = User.objects.get(id=request.POST.get("sponsor_id", _user.id))
            _business_rep = User.objects.get(id=request.POST.get("business_rep_id", _user.id))
            _chief_reviewer = User.objects.get(id=request.POST.get("chief_reviewer_id", _user.id))
            _purchasing_rep = User.objects.get(id=request.POST.get("purchasing_rep_id", _user.id))
            _peer_reviewer = User.objects.get(id=request.POST.get("peer_reviewer_id", _user.id))
            _user_rep = User.objects.get(id=request.POST.get("user_rep_id", _user.id))
            _qc = User.objects.get(id=request.POST.get("qc_id", _user.id))
            _project.sponsor = _sponsor
            _project.current_handler = _sponsor
            _project.business_rep = _business_rep
            _project.chief_reviewer = _chief_reviewer
            _project.purchasing_rep = _purchasing_rep
            _project.peer_reviewer = _peer_reviewer
            _project.user_rep = _user_rep
            _project.qc = _qc
            _hardware_cost = request.POST.get("hardware_cost", "0.0")
            _software_cost = request.POST.get("software_cost", "0.0")
            _other_cost = request.POST.get("other_cost", "0.0")
            _annual_license_cost = request.POST.get("annual_license_cost", "0.0")
            _other_annual_cost = request.POST.get("other_annual_cost", "0.0")
            _project.hardware_cost = _hardware_cost
            _project.software_cost = _software_cost
            _project.other_cost = _other_cost
            _project.annual_license_cost = _annual_license_cost
            _project.other_annual_cost = _other_annual_cost
            # project stakeholders
            _stakeholders = request.POST.getlist("stakeholders", [])
            for _stakeholder_id in _stakeholders:
                if _stakeholder_id:
                    _stakeholder = User.objects.get(id=_stakeholder_id)
                    _project.stakeholders.add(_stakeholder)
            _project.save()
            create_kcp_tasks(_project)
            _msg = '我创建了项目【%s】%s %s' % (
            _project.no, _project.name, pmp.settings.SAAS_PORTAL + '/projectlist/' + str(_project.id))
            send_circle_msg(_user, _msg)
            return HttpResponseRedirect('/projectlist/' + str(_project.id))
        # Show create UI for GET request
        _curdate = datetime.date.today().strftime("%Y-%m-%d")
        _default_end_date = (datetime.date.today() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        return render(request, 'pcreate_1.html',
                      {'current_user': _user, 'curdate': _curdate, 'default_end_date': _default_end_date})
    return HttpResponseRedirect('/login')


def project_approval_view(request):
    _user = get_valid_user(request)
    if _user:
        _pid = request.POST.get("pid")
        _project = Project.objects.get(id=_pid)
        if _user == _project.current_handler:
            _do = request.POST.get("do", "")
            _trustee_id = request.POST.get("trustee_id", "")
            _option = _project.status.status_options.get(do=_do)
            _remarks = request.POST.get("remarks", "")
            handle_project_approval(_project, _user, _option, _trustee_id, _remarks)
            return HttpResponseRedirect('/projectlist/' + str(_project.id))
    return HttpResponseRedirect('/login')


def show_project_list(request, pid):
    _user = get_valid_user(request)
    if _user:
        _teams = _user.member_teams.all()
        if not _teams:
            messages.add_message(request, messages.INFO, '您目前不属于任何团队，请先创建团队或加入现有团队！')
            return render(request, 'teamlist.html', {'current_user': _user})
        _default_team = _user.get_default_team()
        if request.method == "POST":
            _team_id = request.POST.get("team_id", "")
            _default_team = Team.objects.get(id=_team_id)
            _user.default_team = _default_team
            _user.save()
        _to_handle_projects = _user.current_handler_projects.filter(team=_default_team)
        _todo_projects = _default_team.team_projects.filter(phase__ready_state='PLAN')
        _process_projects = _default_team.team_projects.exclude(phase__ready_state='PLAN').exclude(
            phase__ready_state='CLOSE')
        _done_projects = _default_team.team_projects.filter(phase__ready_state='CLOSE', actual_end_date__gt=(datetime.date.today()-datetime.timedelta(days=365))).order_by('-actual_end_date')
        _current_project_id = pid
        return render(request, 'projectlist.html', {'current_user': _user,
                                                    'teams': _teams,
                                                    'default_team': _default_team,
                                                    'handler_projects': _to_handle_projects,
                                                    'todo_projects': _todo_projects,
                                                    'process_projects': _process_projects,
                                                    'done_projects': _done_projects,
                                                    'current_project_id': _current_project_id})
    return HttpResponseRedirect('/login')
