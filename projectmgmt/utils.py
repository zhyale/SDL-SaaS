# coding=utf-8
from usermgmt.models import User
from models import ProjectApproval
from msgmgmt.utils import send_circle_msg, send_msg
import pmp.settings
import datetime


def get_user_by_project_role(current_project, role):
    if role == "PM":
        return current_project.manager
    elif role == "ARCHITECT":
        return current_project.architect or current_project.manager
    elif role == "DEV_REP":
        return current_project.dev_rep or current_project.manager
    elif role == "TEST_REP":
        return current_project.test_rep or current_project.manager
    elif role == "OP_REP":
        return current_project.op_rep or current_project.manager
    elif role == "SECURITY_REVIEWER":
        return current_project.security_reviewer or current_project.manager
    elif role == "SPONSOR":
        return current_project.sponsor or current_project.manager
    elif role == "CHIEF_REVIEWER":
        return current_project.chief_reviewer or current_project.manager
    elif role == "SECURITY_REP":
        return current_project.security_rep or current_project.manager
    elif role == "PEER_REVIEWER":
        return current_project.peer_reviewer or current_project.manager
    elif role == "BUSINESS_REP":
        return current_project.business_rep or current_project.manager
    elif role == "USER_REP":
        return current_project.user_rep or current_project.manager
    elif role == "PURCHASING_REP":
        return current_project.purchasing_rep or current_project.manager
    elif role == "QA":
        return current_project.qa or current_project.manager
    elif role == "QC":
        return current_project.qc or current_project.manager
    elif role == "NONE":
        return None
    return current_project.manager


def handle_project_approval(current_project, current_handler, handle_option, trustee_id, handle_remarks):
    _trustee=None
    if handle_option.do == "TRANSFER":
        if trustee_id:
            _trustee=User.objects.get(id=trustee_id)
            current_project.current_handler = _trustee
    elif handle_option.do == "SUBMIT":
        current_project.status = current_project.phase.phase_statuses.get(status='IN_APPROVAL')
        current_project.current_handler = get_user_by_project_role(current_project, current_project.status.handler_role)
    elif handle_option.do == "APPROVE":
        current_project.phase = current_project.phase.next_phase
        if current_project.phase.ready_state == 'CLOSE':
            project_status = current_project.phase.phase_statuses.get(status='IN_OPERATION')
            current_project.actual_end_date=datetime.date.today()
        else:
            project_status = current_project.phase.phase_statuses.get(status='IN_PROCESS')
        current_project.status = project_status
        current_project.current_handler = get_user_by_project_role(current_project, current_project.status.handler_role)
    elif handle_option.do == "RETURN":
        current_project.status = current_project.phase.phase_statuses.get(status='IN_PROCESS')
        current_project.current_handler = get_user_by_project_role(current_project, current_project.status.handler_role)
    current_project.save()
    ProjectApproval.objects.create(handler=current_handler, project=current_project, option=handle_option,
                                   remarks=handle_remarks, trustee=_trustee)
    project_url = pmp.settings.SAAS_PORTAL + '/projectlist/' + str(current_project.id)
    msg_body = '我审批了项目【%s】%s 审批意见：%s 补充意见：%s 链接: %s  ' % (
    current_project.no, current_project.name, handle_option.opinion, handle_remarks, project_url)
    send_circle_msg(current_handler, msg_body)
    if current_project.current_handler:
        send_msg(current_handler, current_project.current_handler, msg_body+' 请您查看并处理或审批！')
    return


def has_view_privileges_for_project(_project, _user):
    if _user in _project.team.members.all():
            return True
    elif _user == _project.current_handler:
        return True
    elif _user in _project.stakeholders.all():
        return True
    return False
