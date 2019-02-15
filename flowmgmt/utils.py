# coding=utf-8
from models import ProjectFlow, Phase, ProjectPhase, ProjectStatus, ProjectOption, TaskFlow, TaskStatus, TaskOption
import json


def project_flow_list(fid):
    flow = ProjectFlow.objects.get(id=fid)
    phase_list = []
    current_phase = flow.first_phase
    while current_phase:
        current_phase_dict = {'phase': current_phase.id}
        current_phase_dict['display'] = current_phase.phase.name
        statuses = current_phase.phase_statuses.all()
        statuses_dict = {}
        for status in statuses:
            status_dict = {}
            status_dict['description'] = status.description
            status_dict['handler'] = status.handler_role
            options_dict = {}
            options = status.status_options.all()
            for option in options:
                options_dict[option.do] = option.opinion
            status_dict['options'] = options_dict
            statuses_dict[status.status] = status_dict
        current_phase_dict['status'] = statuses_dict
        phase_list.append(current_phase_dict)
        current_phase = current_phase.next_phase
    return phase_list


def project_flow_json(fid):
    phase_list=project_flow_list(fid)
    return json.dumps(phase_list, ensure_ascii=False)


def init_phase():
    if Phase.objects.count()==0:
        Phase.objects.bulk_create([
            Phase(name='立项规划阶段'),
            Phase(name='需求分析阶段'),
            Phase(name='选型阶段'),
            Phase(name='概要设计阶段'),
            Phase(name='方案设计阶段'),
            Phase(name='开发测试阶段'),
            Phase(name='产品发布阶段'),
            Phase(name='验证测试阶段'),
            Phase(name='产品实施阶段'),
            Phase(name='验收阶段'),
            Phase(name='推行阶段'),
            Phase(name='结束/运维阶段'),
        ])


def init_agile_project_flow():
    try:
        # 精简安全内控项目管理流程
        project_flow = ProjectFlow.objects.get(type='AGL')
    except:
        project_flow = ProjectFlow.objects.create(name='精简安全内控项目管理流程', type='AGL')
        # 开发/测试阶段
        phase = Phase.objects.get(name='开发测试阶段', team=None)
        project_phase = ProjectPhase.objects.create(ready_state='PROCESS', flow=project_flow, phase=phase, sort_no=100)
        # 开发/测试阶段 进行态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_PROCESS', handler_role='PM',
                                                      description='单元测试/SIT/安全测试/安全自检')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='SUBMIT', opinion='申请发布，请审核'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        # 开发/测试阶段 审批态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_APPROVAL', handler_role='QA',
                                                      description='QA审核')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='APPROVE', opinion='同意发布'),
            ProjectOption(status=project_status, do='RETURN', opinion='返回改进'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        # 添加KCP任务
        task_flow=TaskFlow.objects.get(type='SEC_DESIGN')
        project_phase.kcp_flows.add(task_flow)
        task_flow=TaskFlow.objects.get(type='SEC_DEV')
        project_phase.kcp_flows.add(task_flow)
        task_flow=TaskFlow.objects.get(type='SEC_TEST')
        project_phase.kcp_flows.add(task_flow)
        project_phase.save()
        # 实施/发布阶段
        #
        phase = Phase.objects.get(name='产品发布阶段', team=None)
        project_phase = ProjectPhase.objects.create(ready_state='PROCESS', flow=project_flow, phase=phase, sort_no=200)
        # 实施/发布阶段 进行态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_PROCESS', handler_role='PM',
                                                      description='发布/安全配置/备份/修改口令')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='SUBMIT', opinion='已完成发布，申请转运维'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        # 实施/发布阶段 审批态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_APPROVAL', handler_role='QA',
                                                      description='QA审核')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='APPROVE', opinion='验收通过'),
            ProjectOption(status=project_status, do='RETURN', opinion='返回改进'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        #
        task_flow=TaskFlow.objects.get(type='SEC_DEPLOY')
        project_phase.kcp_flows.add(task_flow)
        task_flow=TaskFlow.objects.get(type='ACCEPT')
        project_phase.kcp_flows.add(task_flow)
        project_phase.save()
        # 结束/运维阶段
        #
        phase = Phase.objects.get(name='结束/运维阶段', team=None)
        project_phase = ProjectPhase.objects.create(ready_state='CLOSE', flow=project_flow, phase=phase, sort_no=300)
        ProjectStatus.objects.create(phase=project_phase, status='IN_OPERATION', handler_role='NONE', description='项目关闭')
        # 设置联系
        build_phases_relationship(project_flow)


def init_app_project_flow():
    try:
        # 应用开发安全内控项目管理流程
        project_flow = ProjectFlow.objects.get(type='APP')
    except:
        project_flow = ProjectFlow.objects.create(name='应用开发安全内控项目管理流程', type='APP')
        # 立项规划阶段
        phase = Phase.objects.get(name='立项规划阶段', team=None)
        project_phase = ProjectPhase.objects.create(ready_state='PLAN', flow=project_flow, phase=phase, sort_no=100)
        # 立项规划阶段 进行态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_PROCESS', handler_role='PM',
                                                      description='可行性分析及人力/进度/成本估算')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='SUBMIT', opinion='申请立项'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        # 立项规划阶段 审批态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_APPROVAL', handler_role='SPONSOR',
                                                      description='Sponsor审批立项')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='APPROVE', opinion='同意立项，授权项目经理使用组织资源来达成项目目标'),
            ProjectOption(status=project_status, do='RETURN', opinion='返回改进'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        # 需求分析阶段
        phase = Phase.objects.get(name='需求分析阶段', team=None)
        project_phase = ProjectPhase.objects.create(ready_state='PROCESS', flow=project_flow, phase=phase, sort_no=200)
        # 需求分析阶段 进行态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_PROCESS', handler_role='PM',
                                                      description='输出需求分析报告')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='SUBMIT', opinion='申请切换到下一阶段'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        # 需求分析阶段 审批态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_APPROVAL', handler_role='QA',
                                                      description='QA审核本阶段任务完成情况（需求是否经业务确认等）')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='APPROVE', opinion='同意切换到下一阶段'),
            ProjectOption(status=project_status, do='RETURN', opinion='返回改进'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_flow=TaskFlow.objects.get(type='REQ_CONFIRM')
        project_phase.kcp_flows.add(task_flow)
        project_phase.save()
        # 概要设计阶段
        phase = Phase.objects.get(name='概要设计阶段', team=None)
        project_phase = ProjectPhase.objects.create(ready_state='PROCESS', flow=project_flow, phase=phase, sort_no=300)
        # 概要设计阶段 进行态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_PROCESS', handler_role='PM',
                                                      description='方案概要设计/安全自检')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='SUBMIT', opinion='提交审核'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        # 概要设计阶段 审批态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_APPROVAL', handler_role='QA',
                                                      description='QA审核本阶段任务完成情况（方案评审等）')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='APPROVE', opinion='同意切换到下一阶段'),
            ProjectOption(status=project_status, do='RETURN', opinion='返回改进'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_flow=TaskFlow.objects.get(type='SEC_DESIGN')
        project_phase.kcp_flows.add(task_flow)
        task_flow=TaskFlow.objects.get(type='DESIGN_TR')
        project_phase.kcp_flows.add(task_flow)
        project_phase.save()
        # 开发/测试阶段
        phase = Phase.objects.get(name='开发测试阶段', team=None)
        project_phase = ProjectPhase.objects.create(ready_state='PROCESS', flow=project_flow, phase=phase, sort_no=400)
        # 开发/测试阶段 进行态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_PROCESS', handler_role='PM',
                                                      description='详细设计/开发/单元测试/SIT/安全测试')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='SUBMIT', opinion='提交审核'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        # 开发/测试阶段 审批态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_APPROVAL', handler_role='QA',
                                                      description='QA审核本阶段任务完成情况（安全审核等)')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='APPROVE', opinion='同意发布'),
            ProjectOption(status=project_status, do='RETURN', opinion='返回改进'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_flow=TaskFlow.objects.get(type='SEC_DEV')
        project_phase.kcp_flows.add(task_flow)
        task_flow=TaskFlow.objects.get(type='SEC_TEST')
        project_phase.kcp_flows.add(task_flow)
        task_flow=TaskFlow.objects.get(type='PUBLISH_TR')
        project_phase.kcp_flows.add(task_flow)
        project_phase.save()
        # 实施/发布阶段
        #
        phase = Phase.objects.get(name='产品发布阶段', team=None)
        project_phase = ProjectPhase.objects.create(ready_state='PROCESS', flow=project_flow, phase=phase, sort_no=500)
        # 实施/发布阶段 进行态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_PROCESS', handler_role='PM',
                                                      description='服务器安全配置/防火墙策略')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='SUBMIT', opinion='申请验收'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        # 实施/发布阶段 审批态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_APPROVAL', handler_role='QA',
                                                      description='QA审核本阶段任务完成情况（确认实施结果')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='APPROVE', opinion='同意进入验收阶段'),
            ProjectOption(status=project_status, do='RETURN', opinion='返回改进'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_flow=TaskFlow.objects.get(type='SEC_DEPLOY')
        project_phase.kcp_flows.add(task_flow)
        project_phase.save()
        # 验收阶段
        phase = Phase.objects.get(name='验收阶段', team=None)
        project_phase = ProjectPhase.objects.create(ready_state='PROCESS', flow=project_flow, phase=phase, sort_no=600)
        # 验收阶段 进行态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_PROCESS', handler_role='PM',
                                                      description='CMDB更新/备份协议/备份/恢复演练/修改口令/UAT测试')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='SUBMIT', opinion='申请转运维'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        # 验收阶段 审批态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_APPROVAL', handler_role='SPONSOR',
                                                      description='Sponsor确认验收')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='APPROVE', opinion='验收通过，同意转运维'),
            ProjectOption(status=project_status, do='RETURN', opinion='返回改进'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_flow=TaskFlow.objects.get(type='ACCEPT')
        project_phase.kcp_flows.add(task_flow)
        project_phase.save()
        #
        # 结束/运维阶段
        #
        phase = Phase.objects.get(name='结束/运维阶段', team=None)
        project_phase = ProjectPhase.objects.create(ready_state='CLOSE', flow=project_flow, phase=phase, sort_no=700)
        ProjectStatus.objects.create(phase=project_phase, status='IN_OPERATION', handler_role='NONE')
        # 设置联系
        build_phases_relationship(project_flow)


def init_inf_project_flow():
    try:
        # 外购产品实施安全内控项目管理流程
        project_flow = ProjectFlow.objects.get(type='INF')
    except:
        project_flow = ProjectFlow.objects.create(name='外购产品实施安全内控项目管理流程', type='INF')
        # 立项规划阶段
        phase = Phase.objects.get(name='立项规划阶段', team=None)
        project_phase = ProjectPhase.objects.create(ready_state='PLAN', flow=project_flow, phase=phase, sort_no=100)
        # 立项规划阶段 进行态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_PROCESS', handler_role='PM',
                                                      description='可行性分析及人力/进度/成本估算')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='SUBMIT', opinion='申请立项'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        # 立项规划阶段 审批态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_APPROVAL', handler_role='SPONSOR',
                                                      description='Sponsor审批立项')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='APPROVE', opinion='同意立项，授权项目经理使用组织资源来达成项目目标'),
            ProjectOption(status=project_status, do='RETURN', opinion='返回改进'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        # 需求分析阶段
        phase = Phase.objects.get(name='需求分析阶段', team=None)
        project_phase = ProjectPhase.objects.create(ready_state='PROCESS', flow=project_flow, phase=phase, sort_no=200)
        # 需求分析阶段 进行态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_PROCESS', handler_role='PM',
                                                      description='输出需求分析报告')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='SUBMIT', opinion='申请切换到下一阶段'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        # 需求分析阶段 审批态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_APPROVAL', handler_role='QA',
                                                      description='QA审核')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='APPROVE', opinion='同意切换到下一阶段'),
            ProjectOption(status=project_status, do='RETURN', opinion='返回改进'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_flow=TaskFlow.objects.get(type='REQ_CONFIRM')
        project_phase.kcp_flows.add(task_flow)
        project_phase.save()
        # 选型阶段
        phase = Phase.objects.get(name='选型阶段', team=None)
        project_phase = ProjectPhase.objects.create(ready_state='PROCESS', flow=project_flow, phase=phase, sort_no=300)
        # 选型阶段 进行态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_PROCESS', handler_role='PM',
                                                      description='选型机制/评分标准/选型DCP')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='SUBMIT', opinion='本阶段任务完成，申请切换到下一阶段'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        # 选型阶段 审批态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_APPROVAL', handler_role='QA',
                                                      description='QA审核')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='APPROVE', opinion='同意切换到下一阶段'),
            ProjectOption(status=project_status, do='RETURN', opinion='返回改进'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_flow=TaskFlow.objects.get(type='BID')
        project_phase.kcp_flows.add(task_flow)
        project_phase.save()
        # 方案设计阶段
        phase = Phase.objects.get(name='方案设计阶段', team=None)
        project_phase = ProjectPhase.objects.create(ready_state='PROCESS', flow=project_flow, phase=phase, sort_no=400)
        # 方案设计阶段 进行态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_PROCESS', handler_role='PM',
                                                      description='方案概要设计/安全自检')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='SUBMIT', opinion='提交审核'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        # 方案设计阶段 审批态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_APPROVAL', handler_role='QA',
                                                      description='QA审核')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='APPROVE', opinion='同意进入下一阶段'),
            ProjectOption(status=project_status, do='RETURN', opinion='返回改进'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_flow=TaskFlow.objects.get(type='SEC_DESIGN')
        project_phase.kcp_flows.add(task_flow)
        task_flow=TaskFlow.objects.get(type='DESIGN_TR')
        project_phase.kcp_flows.add(task_flow)
        project_phase.save()
        # 验证测试阶段
        phase = Phase.objects.get(name='验证测试阶段', team=None)
        project_phase = ProjectPhase.objects.create(ready_state='PROCESS', flow=project_flow, phase=phase, sort_no=500)
        # 验证测试阶段 进行态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_PROCESS', handler_role='PM',
                                                      description='在测试环境进行测试验证')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='SUBMIT', opinion='申请实施'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        # 验证测试阶段 审批态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_APPROVAL', handler_role='QA',
                                                      description='QA审核')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='APPROVE', opinion='同意实施'),
            ProjectOption(status=project_status, do='RETURN', opinion='返回改进'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_flow=TaskFlow.objects.get(type='SEC_TEST')
        project_phase.kcp_flows.add(task_flow)
        task_flow=TaskFlow.objects.get(type='PUBLISH_TR')
        project_phase.kcp_flows.add(task_flow)
        project_phase.save()
        # 产品实施阶段
        phase = Phase.objects.get(name='产品实施阶段', team=None)
        project_phase = ProjectPhase.objects.create(ready_state='PROCESS', flow=project_flow, phase=phase, sort_no=600)
        # 产品实施阶段 进行态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_PROCESS', handler_role='PM',
                                                      description='服务器安全配置/防火墙策略')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='SUBMIT', opinion='申请验收'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        # 产品实施阶段 审批态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_APPROVAL', handler_role='QA',
                                                      description='QA审核')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='APPROVE', opinion='同意进入验收阶段'),
            ProjectOption(status=project_status, do='RETURN', opinion='返回改进'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_flow=TaskFlow.objects.get(type='SEC_DEPLOY')
        project_phase.kcp_flows.add(task_flow)
        project_phase.save()
        # 验收阶段
        phase = Phase.objects.get(name='验收阶段', team=None)
        project_phase = ProjectPhase.objects.create(ready_state='PROCESS', flow=project_flow, phase=phase, sort_no=700)
        # 验收阶段 进行态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_PROCESS', handler_role='PM',
                                                      description='CMDB更新/备份协议/备份/恢复演练/修改口令/UAT测试')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='SUBMIT', opinion='申请转运维'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        # 验收阶段 审批态
        project_status = ProjectStatus.objects.create(phase=project_phase, status='IN_APPROVAL', handler_role='SPONSOR',
                                                      description='Sponsor确认验收')
        ProjectOption.objects.bulk_create([
            ProjectOption(status=project_status, do='APPROVE', opinion='验收通过，同意转运维'),
            ProjectOption(status=project_status, do='RETURN', opinion='返回改进'),
            ProjectOption(status=project_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_flow=TaskFlow.objects.get(type='ACCEPT')
        project_phase.kcp_flows.add(task_flow)
        project_phase.save()
        #
        # 结束/运维阶段
        #
        phase = Phase.objects.get(name='结束/运维阶段', team=None)
        project_phase = ProjectPhase.objects.create(ready_state='CLOSE', flow=project_flow, phase=phase, sort_no=800)
        ProjectStatus.objects.create(phase=project_phase, status='IN_OPERATION', handler_role='NONE')
        # 设置联系
        build_phases_relationship(project_flow)


def build_phases_relationship(project_flow):
    phases=project_flow.projectphase_set.order_by('sort_no')
    project_flow.first_phase = phases[0]
    for i in range(0, len(phases)-1):
        phases[i].next_phase=phases[i+1]
        phases[i].save()
    project_flow.save()


def task_flow_list(fid):
    flow = TaskFlow.objects.get(id=fid)
    status_list = []
    current_status = flow.first_status
    while current_status:
        current_status_dict = {'status': current_status.id}
        current_status_dict['display'] = current_status.name
        current_status_dict['description'] = current_status.description
        current_status_dict['handler'] = current_status.handler_role
        options_dict = {}
        options = current_status.status_options.all()
        for option in options:
            options_dict[option.do] = option.opinion
        current_status_dict['options'] = options_dict
        status_list.append(current_status_dict)
        current_status = current_status.next_status
    return status_list


def task_flow_json(fid):
    status_list=task_flow_list(fid)
    return json.dumps(status_list, ensure_ascii=False)


def init_general_task_flow():
    try:
        task_flow=TaskFlow.objects.get(type='GEN')
    except:
        task_flow=TaskFlow.objects.create(name='通用任务', type='GEN', description='无特定流程的通用任务')
        task_status=TaskStatus.objects.create(name='任务待执行', flow=task_flow, sort_no=100,
                                              handler_role='TASK_LEADER',
                                              ready_state='TODO', description='任务未启动')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='APPROVE', opinion='启动任务'),
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='任务执行中', flow=task_flow, sort_no=200,
                                              handler_role='TASK_LEADER',
                                              ready_state='PROCESSING', description='任务执行中')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='提交复核'),
            TaskOption(status=task_status, do='RETURN', opinion='任务暂停，稍后处理'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='任务复核中', flow=task_flow, sort_no=300,
                                              handler_role='TASK_REVIEWER',
                                              ready_state='REVIEW', description='任务复核中')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='复核通过'),
            TaskOption(status=task_status, do='RETURN', opinion='返回改进'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        TaskStatus.objects.create(name='任务已完成', flow=task_flow, sort_no=400,
                                  handler_role='NONE',
                                  ready_state='DONE', description='任务结束')
        build_statuses_relationship(task_flow)


def init_teamwork_task_flow():
    try:
        task_flow=TaskFlow.objects.get(type='TEAMWORK')
    except:
        task_flow=TaskFlow.objects.create(name='协作任务', type='TEAMWORK', description='不需要复核的任务')
        task_status=TaskStatus.objects.create(name='任务待执行', flow=task_flow, sort_no=100,
                                              handler_role='TASK_LEADER',
                                              ready_state='TODO', description='任务未启动')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='APPROVE', opinion='启动任务'),
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='任务执行中', flow=task_flow, sort_no=200,
                                              handler_role='TASK_LEADER',
                                              ready_state='PROCESSING', description='任务执行中')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='任务已完成'),
            TaskOption(status=task_status, do='RETURN', opinion='任务暂停，稍后处理'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        TaskStatus.objects.create(name='任务已完成', flow=task_flow, sort_no=300,
                                  handler_role='NONE',
                                  ready_state='DONE', description='任务结束')
        build_statuses_relationship(task_flow)


def init_sec_design_check_workflow():
    try:
        task_flow=TaskFlow.objects.get(type='SEC_DESIGN')
    except:
        task_flow=TaskFlow.objects.create(name='安全设计自检', type='SEC_DESIGN',  description='产品架构/方案设计的安全性自检')
        task_status=TaskStatus.objects.create(name='待执行安全自检', flow=task_flow, sort_no=100,
                                              handler_role='ARCHITECT',
                                              ready_state='TODO', description='任务未启动')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='APPROVE', opinion='启动任务'),
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='自检进行中', flow=task_flow, sort_no=200,
                                              handler_role='ARCHITECT',
                                              ready_state='PROCESSING', description='对照安全Checklist逐条检查')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='提交复核'),
            TaskOption(status=task_status, do='RETURN', opinion='任务暂停，稍后处理'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='复核与风险评估', flow=task_flow, sort_no=300,
                                              handler_role='SECURITY_REVIEWER',
                                              ready_state='REVIEW', description='根据自检结果，结合业务场景给出风险评估意见')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='复核通过'),
            TaskOption(status=task_status, do='RETURN', opinion='返回改进'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        TaskStatus.objects.create(name='完成安全自检', flow=task_flow, sort_no=400,
                                  handler_role='NONE',
                                  ready_state='DONE', description='任务结束')
        build_statuses_relationship(task_flow)


def init_design_tr_check_workflow():
    try:
        task_flow=TaskFlow.objects.get(type='DESIGN_TR')
    except:
        task_flow=TaskFlow.objects.create(name='方案设计评审自检', type='DESIGN_TR',  description='产品架构/方案设计的综合自检')
        task_status=TaskStatus.objects.create(name='待执行安全自检', flow=task_flow, sort_no=100,
                                              handler_role='ARCHITECT',
                                              ready_state='TODO', description='任务未启动')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='APPROVE', opinion='启动任务'),
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='自检进行中', flow=task_flow, sort_no=200,
                                              handler_role='ARCHITECT',
                                              ready_state='PROCESSING', description='对照Checklist逐条检查')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='提交复核'),
            TaskOption(status=task_status, do='RETURN', opinion='任务暂停，稍后处理'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='评审与复核', flow=task_flow, sort_no=300,
                                              handler_role='CHIEF_REVIEWER',
                                              ready_state='REVIEW', description='结合自检结果，给出评审意见')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='复核通过'),
            TaskOption(status=task_status, do='RETURN', opinion='返回改进'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        TaskStatus.objects.create(name='完成TR', flow=task_flow, sort_no=400,
                                  handler_role='NONE',
                                  ready_state='DONE', description='任务结束')
        build_statuses_relationship(task_flow)


def init_publish_tr_check_workflow():
    try:
        task_flow=TaskFlow.objects.get(type='PUBLISH_TR')
    except:
        task_flow=TaskFlow.objects.create(name='上线/发布评审自检', type='PUBLISH_TR',  description='上线前的综合自检')
        task_status=TaskStatus.objects.create(name='待执行安全自检', flow=task_flow, sort_no=100,
                                              handler_role='ARCHITECT',
                                              ready_state='TODO', description='任务未启动')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='APPROVE', opinion='启动任务'),
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='自检进行中', flow=task_flow, sort_no=200,
                                              handler_role='ARCHITECT',
                                              ready_state='PROCESSING', description='对照Checklist逐条检查')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='提交复核'),
            TaskOption(status=task_status, do='RETURN', opinion='任务暂停，稍后处理'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='评审与复核', flow=task_flow, sort_no=300,
                                              handler_role='CHIEF_REVIEWER',
                                              ready_state='REVIEW', description='结合自检结果，给出评审意见')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='复核通过'),
            TaskOption(status=task_status, do='RETURN', opinion='返回改进'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        TaskStatus.objects.create(name='完成TR', flow=task_flow, sort_no=400,
                                  handler_role='NONE',
                                  ready_state='DONE', description='任务结束')
        build_statuses_relationship(task_flow)


def init_sec_dev_check_workflow():
    try:
        task_flow=TaskFlow.objects.get(type='SEC_DEV')
    except:
        task_flow=TaskFlow.objects.create(name='安全开发自检', type='SEC_DEV',  description='代码的安全性自检')
        task_status=TaskStatus.objects.create(name='待执行安全自检', flow=task_flow, sort_no=100,
                                              handler_role='DEV_REP',
                                              ready_state='TODO', description='任务未启动')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='APPROVE', opinion='启动任务'),
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='自检进行中', flow=task_flow, sort_no=200,
                                              handler_role='DEV_REP',
                                              ready_state='PROCESSING', description='对照安全Checklist逐条检查')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='提交复核'),
            TaskOption(status=task_status, do='RETURN', opinion='任务暂停，稍后处理'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='复核与风险评估', flow=task_flow, sort_no=300,
                                              handler_role='SECURITY_REVIEWER',
                                              ready_state='REVIEW', description='根据自检结果，结合业务场景给出风险评估意见')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='复核通过'),
            TaskOption(status=task_status, do='RETURN', opinion='返回改进'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        TaskStatus.objects.create(name='完成安全自检', flow=task_flow, sort_no=400,
                                  handler_role='NONE',
                                  ready_state='DONE', description='任务结束')
        build_statuses_relationship(task_flow)


def init_sec_test_check_workflow():
    try:
        task_flow=TaskFlow.objects.get(type='SEC_TEST')
    except:
        task_flow=TaskFlow.objects.create(name='安全测试自检', type='SEC_TEST',  description='安全测试方法/用例自检')
        task_status=TaskStatus.objects.create(name='待执行安全自检', flow=task_flow, sort_no=100,
                                              handler_role='TEST_REP',
                                              ready_state='TODO', description='任务未启动')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='APPROVE', opinion='启动任务'),
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='自检进行中', flow=task_flow, sort_no=200,
                                              handler_role='TEST_REP',
                                              ready_state='PROCESSING', description='对照安全Checklist逐条检查')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='提交复核'),
            TaskOption(status=task_status, do='RETURN', opinion='任务暂停，稍后处理'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='复核与风险评估', flow=task_flow, sort_no=300,
                                              handler_role='SECURITY_REVIEWER',
                                              ready_state='REVIEW', description='根据自检结果，结合业务场景给出风险评估意见')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='复核通过'),
            TaskOption(status=task_status, do='RETURN', opinion='返回改进'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        TaskStatus.objects.create(name='完成安全自检', flow=task_flow, sort_no=400,
                                  handler_role='NONE',
                                  ready_state='DONE', description='任务结束')
        build_statuses_relationship(task_flow)


def init_sec_deploy_check_workflow():
    try:
        task_flow=TaskFlow.objects.get(type='SEC_DEPLOY')
    except:
        task_flow=TaskFlow.objects.create(name='安全部署自检', type='SEC_DEPLOY',  description='部署/实施/配置的安全性自检')
        task_status=TaskStatus.objects.create(name='待执行安全自检', flow=task_flow, sort_no=100,
                                              handler_role='OP_REP',
                                              ready_state='TODO', description='任务未启动')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='APPROVE', opinion='启动任务'),
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='自检进行中', flow=task_flow, sort_no=200,
                                              handler_role='OP_REP',
                                              ready_state='PROCESSING', description='对照安全Checklist逐条检查')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='提交复核'),
            TaskOption(status=task_status, do='RETURN', opinion='任务暂停，稍后处理'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='复核与风险评估', flow=task_flow, sort_no=300,
                                              handler_role='SECURITY_REVIEWER',
                                              ready_state='REVIEW', description='根据自检结果，给出风险评估意见')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='复核通过'),
            TaskOption(status=task_status, do='RETURN', opinion='返回改进'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        TaskStatus.objects.create(name='完成安全自检', flow=task_flow, sort_no=400,
                                  handler_role='NONE',
                                  ready_state='DONE', description='任务结束')
        build_statuses_relationship(task_flow)


def init_acceptance_check_workflow():
    try:
        task_flow=TaskFlow.objects.get(type='ACCEPT')
    except:
        task_flow=TaskFlow.objects.create(name='验收', type='ACCEPT',  description='CMDB/备份/口令回收/UAT测试自检')
        task_status=TaskStatus.objects.create(name='待执行验收', flow=task_flow, sort_no=100,
                                              handler_role='OP_REP',
                                              ready_state='TODO', description='验收未启动')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='APPROVE', opinion='启动验收任务'),
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='验收进行中', flow=task_flow, sort_no=200,
                                              handler_role='OP_REP',
                                              ready_state='PROCESSING', description='CMDB更新/备份协议/备份/恢复演练/修改口令/UAT测试')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='提交复核'),
            TaskOption(status=task_status, do='RETURN', opinion='任务暂停，稍后处理'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='复核中', flow=task_flow, sort_no=300,
                                              handler_role='PM',
                                              ready_state='REVIEW', description='审核验收各任务完成情况')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='复核通过'),
            TaskOption(status=task_status, do='RETURN', opinion='返回改进'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        TaskStatus.objects.create(name='完成验收任务', flow=task_flow, sort_no=400,
                                  handler_role='NONE',
                                  ready_state='DONE', description='任务结束')
        build_statuses_relationship(task_flow)


def init_req_confirm_task_flow():
    try:
        task_flow=TaskFlow.objects.get(type='REQ_CONFIRM')
    except:
        task_flow=TaskFlow.objects.create(name='需求确认', type='REQ_CONFIRM', description='确认项目需求')
        task_status=TaskStatus.objects.create(name='任务待执行', flow=task_flow, sort_no=100,
                                              handler_role='PM',
                                              ready_state='TODO', description='任务未启动')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='APPROVE', opinion='启动任务'),
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='需求自检中', flow=task_flow, sort_no=200,
                                              handler_role='PM',
                                              ready_state='PROCESSING', description='任务执行中')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='提交复核'),
            TaskOption(status=task_status, do='RETURN', opinion='任务暂停，稍后处理'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='需求确认中', flow=task_flow, sort_no=300,
                                              handler_role='BUSINESS_REP',
                                              ready_state='REVIEW', description='任务复核中')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='复核通过'),
            TaskOption(status=task_status, do='RETURN', opinion='返回改进'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        TaskStatus.objects.create(name='需求确认完成', flow=task_flow, sort_no=400,
                                  handler_role='NONE',
                                  ready_state='DONE', description='任务结束')
        build_statuses_relationship(task_flow)


def init_bid_task_flow():
    try:
        task_flow=TaskFlow.objects.get(type='BID')
    except:
        task_flow=TaskFlow.objects.create(name='选型自检', type='BID', description='确认项目需求')
        task_status=TaskStatus.objects.create(name='任务待执行', flow=task_flow, sort_no=100,
                                              handler_role='PM',
                                              ready_state='TODO', description='任务未启动')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='APPROVE', opinion='启动任务'),
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='自检中', flow=task_flow, sort_no=200,
                                              handler_role='PM',
                                              ready_state='PROCESSING', description='任务执行中')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='提交复核'),
            TaskOption(status=task_status, do='RETURN', opinion='任务暂停，稍后处理'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        task_status=TaskStatus.objects.create(name='复核中', flow=task_flow, sort_no=300,
                                              handler_role='PURCHASING_REP',
                                              ready_state='REVIEW', description='任务复核中')
        TaskOption.objects.bulk_create([
            TaskOption(status=task_status, do='UPDATE', opinion='添加备注'),
            TaskOption(status=task_status, do='APPROVE', opinion='复核通过'),
            TaskOption(status=task_status, do='RETURN', opinion='返回改进'),
            TaskOption(status=task_status, do='TRANSFER', opinion='转他人处理'),
        ])
        TaskStatus.objects.create(name='需求确认完成', flow=task_flow, sort_no=400,
                                  handler_role='NONE',
                                  ready_state='DONE', description='任务结束')
        build_statuses_relationship(task_flow)


def build_statuses_relationship(task_flow):
    statuses=task_flow.flow_statuses.order_by('sort_no')
    task_flow.first_status = statuses[0]
    status_count=len(statuses)
    for i in range(0, status_count):
        if i <= (status_count-2) :
            statuses[i].next_status=statuses[i+1]
        if i>=1:
            statuses[i].pre_status=statuses[i-1]
        statuses[i].save()
    task_flow.save()


def init_flows():
    # init task flows
    init_general_task_flow()
    init_sec_design_check_workflow()
    init_sec_dev_check_workflow()
    init_sec_test_check_workflow()
    init_sec_deploy_check_workflow()
    init_acceptance_check_workflow()
    init_req_confirm_task_flow()
    init_design_tr_check_workflow()
    init_publish_tr_check_workflow()
    init_bid_task_flow()
    init_teamwork_task_flow()
    # init project flows
    init_phase()
    init_agile_project_flow()
    init_app_project_flow()
    init_inf_project_flow()
    return
