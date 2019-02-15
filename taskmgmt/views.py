# coding=utf-8
from django.shortcuts import render
from django.db.models import F
from django.contrib import messages
from usermgmt.utils import get_valid_user
from msgmgmt.utils import send_circle_msg, send_msg
from taskmgmt.models import *
from django.http import HttpResponse, HttpResponseRedirect
import pmp.settings
from pmp.cache import get_task_flow_by_type, get_task_by_id, clear_task_cache_by_id
from utils import handle_task_approval, task_need_approval
import datetime
from django.utils import timezone
import time


def TaskCreate(request):
    _user = get_valid_user(request)
    if _user:
        if request.method == "POST":
            _team_id = request.POST.get("team_id", "")
            if _team_id:
                _default_team = Team.objects.get(id=_team_id)
                _user.default_team = _default_team
                _user.save()
            else:
                _project = None
                _pid = int(request.POST.get("pid", ""))
                if _pid:
                    _project = Project.objects.get(id=_pid)
                _name = request.POST.get("name")
                _description = request.POST.get("description")
                _plan_mandays = float(request.POST.get("plan_mandays"))
                _done_in_project_phase = None
                if _project:
                    _done_in_project_phase = _project.phase
                _deadline = datetime.datetime.strptime(request.POST.get("deadline"), '%Y-%m-%d')
                _leader = User.objects.get(id=request.POST.get("leader_id"))
                _need_review=request.POST.get("need_review", None)
                if _need_review:
                    _flow=get_task_flow_by_type('GEN')
                    _reviewer = User.objects.get(id=request.POST.get("reviewer_id"))
                else:
                    _flow=get_task_flow_by_type('TEAMWORK')
                    _reviewer=_user
                _task = Task.objects.create(name=_name, description=_description,
                                            flow=_flow,
                                            assigner=_user, leader=_leader, reviewer=_reviewer, current_handler=_leader,
                                            plan_mandays=_plan_mandays, project=_project, is_kcp=False,
                                            is_subtask=False,
                                            done_in_project_phase=_done_in_project_phase, deadline=_deadline,
                                            team=_user.default_team,
                                            status=_flow.first_status)
                _members = request.POST.getlist("members", [])
                for member_id in _members:
                    if member_id:
                        _member = User.objects.get(id=member_id)
                        _task.members.add(_member)
                TaskApproval.objects.create(handler=_user, task=_task, remarks='分配任务')
                _task_link = pmp.settings.SAAS_PORTAL + '/tasklist/' + str(_task.id)
                _msg = '我创建了任务：%s %s' % (_task.name, _task_link)
                send_circle_msg(_user, _msg)
                send_msg(_user, _task.current_handler, _msg)
                return HttpResponseRedirect('/tasklist')
        _projects = Project.objects.filter(team=_user.default_team).exclude(phase__ready_state='CLOSE')
        _teams = _user.member_teams.all()
        _flows = TaskFlow.objects.filter(team__isnull=True) | TaskFlow.objects.filter(team=_user.default_team)
        _deadline = (datetime.date.today() + datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        return render(request, 'taskcreate.html',
                      {'current_user': _user, 'projects': _projects, 'teams': _teams, 'flows': _flows,
                       'deadline': _deadline})
    return HttpResponseRedirect('/login')


def task_add_member(request):
    _user = get_valid_user(request)
    if _user:
        _tid=request.POST.get("tid","")
        try:
            _task = Task.objects.get(id=_tid)
        except:
            messages.add_message(request, messages.INFO, '指定的任务不存在！')
            return render(request, 'index.html', {'current_user': _user})
        _member_id=request.POST.get("member_id","")
        try:
            _member = User.objects.get(id=_member_id)
        except:
            messages.add_message(request, messages.INFO, '指定的用户不存在！')
            return render(request, 'index.html', {'current_user': _user})
        _task.members.add(_member)
        _task.save()
        clear_task_cache_by_id(_tid)
        return HttpResponseRedirect('/tasklist/'+_tid)
    return HttpResponseRedirect('/login')

# Not use
def TaskEdit(request, tid):
    _user = get_valid_user(request)
    if _user:
        _handler = _user
        _tid = int(tid)
        try:
            _task = Task.objects.get(id=_tid)
        except:
            messages.add_message(request, messages.INFO, '指定的任务不存在！')
            return render(request, 'index.html', {'current_user': _user})
        if request.method == 'GET':
            _projects = (_handler.manager_projects.exclude(status='IN_OPERATION') | _handler.member_projects.exclude(
                status='IN_OPERATION') | _handler.reviewer_projects.exclude(status='IN_OPERATION')).distinct()
            return render(request, 'taskedit.html', {'current_user': _user, 'task': _task, 'projects': _projects})
        _pid = int(request.POST.get("pid"))
        if _pid:
            _project = Project.objects.get(id=_pid)
        else:
            _project = None
        _is_kcp = request.POST.get("is_kcp")
        if _is_kcp:
            _is_kcp = True
        _done_in_project_phase = None
        if _project:
            _done_in_project_phase = _project.status
        _task.name = request.POST.get("name")
        _task.description = request.POST.get("description")
        _task.assigner = _handler
        _task.leader = User.objects.get(username=request.POST.get("leader"))
        _task.reviewer = User.objects.get(username=request.POST.get("reviewer"))
        _task.plan_mandays = float(request.POST.get("plan_mandays"))
        _task.project = _project
        _task.is_kcp = _is_kcp
        _task.done_in_project_phase = _done_in_project_phase
        _task.save()
        TaskApproval.objects.create(handler=_user, task=_task, remarks='编辑任务')
        return HttpResponseRedirect('/tasklist/' + str(_task.id))
    return HttpResponseRedirect('/login')


def TaskList(request, tid):
    _user = get_valid_user(request)
    if _user:
        _teams = _user.member_teams.all()
        if not _teams:
            messages.add_message(request, messages.INFO, '您目前不属于任何团队，请先创建团队或加入现有团队！')
            return render(request, 'teamlist.html', {'current_user': _user})
        _default_team = _user.get_default_team()
        if request.method == "POST":
            # switch team
            _team_id = request.POST.get("team_id", "")
            _default_team = Team.objects.get(id=_team_id)
            _user.default_team = _default_team
            _user.save()
        _to_handle_team_tasks = _user.current_handler_tasks.filter(team=_default_team)
        _to_handle_tasks = _to_handle_team_tasks.filter(
            project__phase=F('done_in_project_phase')) | _to_handle_team_tasks.filter(project__isnull=True)
        _future_tasks = _to_handle_team_tasks.filter(project__isnull=False).exclude(
            project__phase=F('done_in_project_phase'))
        _todo_tasks_include_future=_default_team.team_tasks.filter(status__ready_state__exact='TODO')
        _todo_tasks = _todo_tasks_include_future.filter(project__phase=F('done_in_project_phase')) | _todo_tasks_include_future.filter(done_in_project_phase__isnull=True)
        _process_tasks = _default_team.team_tasks.exclude(status__ready_state='TODO').exclude(status__ready_state='DONE')
        _done_tasks = _default_team.team_tasks.filter(status__ready_state='DONE', done_time__gt=(timezone.now()-datetime.timedelta(days=30))).order_by('-done_time')
        current_task=get_task_by_id(tid)
        if tid and not current_task:
            messages.add_message(request, messages.INFO, '参数错误！')
        return render(request, 'tasklist.html', {'current_user': _user,
                                                 'teams': _teams,
                                                 'default_team': _default_team,
                                                 'handler_tasks': _to_handle_tasks,
                                                 'future_tasks': _future_tasks,
                                                 'todo_tasks': _todo_tasks,
                                                 'process_tasks': _process_tasks,
                                                 'done_tasks': _done_tasks,
                                                 'current_task': current_task})
    return HttpResponseRedirect('/login')


def TaskListForProject(request, pid):
    _user = get_valid_user(request)
    if _user:
        _project = Project.objects.get(id=pid)
        _default_team = _project.team
        _to_handle_team_tasks = _user.current_handler_tasks.filter(team=_default_team, project=_project)
        _to_handle_tasks = _to_handle_team_tasks.filter(
            project__phase=F('done_in_project_phase')) | _to_handle_team_tasks.filter(project__isnull=True)
        _future_tasks = _to_handle_team_tasks.filter(project__isnull=False).exclude(
            project__phase=F('done_in_project_phase'))
        _todo_tasks = _project.project_tasks.filter(status='IN_TODO').filter(project__phase=F('done_in_project_phase'))
        _process_tasks = _project.project_tasks.filter(status='IN_PROCESS')
        _done_tasks = _project.project_tasks.filter(status='IN_DONE')
        return render(request, 'tasklist.html', {'current_user': _user,
                                                 'teams': [_project.team],
                                                 'default_team': _default_team,
                                                 'handler_tasks': _to_handle_tasks,
                                                 'future_tasks': _future_tasks,
                                                 'todo_tasks': _todo_tasks,
                                                 'process_tasks': _process_tasks,
                                                 'done_tasks': _done_tasks,
                                                 'project': _project})
    return HttpResponseRedirect('/login')


def TaskInfo(request, tid):
    _user = get_valid_user(request)
    if _user:
        _id = int(tid)
        _task=get_task_by_id(_id)
        if not _task:
            messages.add_message(request, messages.INFO, '指定的任务不存在！')
            return render(request, 'index.html', {'current_user': _user})
        _need_review = task_need_approval(_task, _user)
        _can_be_deleted = _task.can_be_deleted_by(_user)
        _check_results = _task.task_checkresults.all()
        _custom_check_results = _task.custom_checkresults.all()
        return render(request, 'taskinfo.html', {'current_user': _user,
                                                 'task': _task,
                                                 'check_results': _check_results,
                                                 'custom_check_results':_custom_check_results,
                                                 'need_review': _need_review,
                                                 'can_be_deleted': _can_be_deleted})
    return HttpResponseRedirect('/login')


def TaskDelete(request):
    _user = get_valid_user(request)
    if _user:
        _tid = request.POST.get("tid")
        if _tid:
            _task = Task.objects.get(id=_tid)
            if _task.can_be_deleted_by(_user):
                _task.delete()
                clear_task_cache_by_id(_tid)
        return HttpResponseRedirect('tasklist')
    return HttpResponseRedirect('/login')


def task_approval_view(request):
    _user = get_valid_user(request)
    if _user:
        _tid = request.POST.get("tid")
        _task = Task.objects.get(id=_tid)
        if _user == _task.current_handler:
            _do = request.POST.get("do","UPDATE")
            _option = _task.status.status_options.get(do=_do)
            _trustee_id = request.POST.get("trustee_id", "")
            _handle_remarks = request.POST.get("remarks", "")
            _actual_mandays = request.POST.get("actual_mandays", 0)
            _task.actual_mandays = float(_actual_mandays)
            handle_task_approval(_task, _user, _option, _trustee_id, _handle_remarks)
            return HttpResponseRedirect('/tasklist/' + _tid)
        elif _user in _task.team.members.all():
            _option = _task.status.status_options.get(do='UPDATE')
            _handle_remarks = request.POST.get("remarks", "")
            handle_task_approval(_task, _user, _option, None, _handle_remarks)
            return HttpResponseRedirect('/tasklist/' + _tid)
    return HttpResponseRedirect('/login')


def check_result(request):
    _user = get_valid_user(request)
    if _user:
        _result_id = request.POST.get("result_id")
        _check_result = CheckResult.objects.get(id=_result_id)
        if _user == _check_result.task.current_handler:
            _result = request.POST.get("result")
            _check_result.result = _result
            _check_result.save()
        return HttpResponse("OK", content_type="text/plain")
    return HttpResponseRedirect('/login')


def custom_check_result(request):
    _user = get_valid_user(request)
    if _user:
        _result_id = request.POST.get("result_id",0)
        _result_id = int(_result_id)
        if _result_id: # update result
            _check_result = CustomCheckResult.objects.get(id=_result_id)
            _task=_check_result.task
            if _user == _task.leader or _user==_task.reviewer or _user in _task.members.all():
                _result = request.POST.get("result")
                _check_result.result = _result
                _check_result.save()
        else: # create new check item
            task_id=request.POST.get("task_id")
            _task=Task.objects.get(id=task_id)
            _check_item=request.POST.get("check_item")
            CustomCheckResult.objects.create(task=_task, check_item=_check_item, result='NONE')
        return HttpResponse("OK", content_type="text/plain")
    return HttpResponseRedirect('/login')


def show_checklist_as_specifications(request):
    _user = get_valid_user(request)
    if _user:
        sec_design_flow = get_task_flow_by_type('SEC_DESIGN')
        design_items = sec_design_flow.flow_check_items.all()
        sec_dev_flow = get_task_flow_by_type('SEC_DEV')
        dev_items = sec_dev_flow.flow_check_items.all()
        sec_test_flow = get_task_flow_by_type('SEC_TEST')
        test_items = sec_test_flow.flow_check_items.all()
        sec_deploy_flow = get_task_flow_by_type('SEC_DEPLOY')
        deploy_items = sec_deploy_flow.flow_check_items.all()
        _user = get_valid_user(request)
        return render(request, 'specifications.html',
                      {'current_user': _user, 'design_rules': design_items, 'dev_rules': dev_items,
                       'test_rules': test_items, 'deploy_rules': deploy_items})
    return HttpResponseRedirect('/login')


def show_kcp_for_project(request):
    _user = get_valid_user(request)
    return render(request, 'kcp.html', {'current_user': _user})
