# coding=utf-8
from flowmgmt.models import TaskFlow
from taskmgmt.models import Task, TaskApproval, CheckResult
from usermgmt.models import User
from msgmgmt.utils import send_msg, send_circle_msg
from projectmgmt.utils import get_user_by_project_role
from models import CheckItem
from pmp.cache import clear_task_cache_by_id
import pmp.settings
import datetime


def task_need_approval(current_task, current_user):
    if current_user == current_task.current_handler:
        current_project = current_task.project
        if current_project:
            if current_task.done_in_project_phase == current_project.phase:
                return True
        else:
            return True
    return False


def init_sec_design_checklist():
    task_flow = TaskFlow.objects.get(type='SEC_DESIGN')
    if task_flow.flow_check_items.count() == 0:
        CheckItem.objects.bulk_create([
            CheckItem(description='前端不能直接访问数据库，应采取三层架构（表现层、业务逻辑层、数据访问层）', flow=task_flow, product_type='GEN',
                      sort_no=100),
            CheckItem(description='应不信任、不依赖客户端的安全控制措施，无论客户端采取何种措施，服务器侧都必须对用户提交的数据进行合法性检测', flow=task_flow,
                      product_type='GEN', sort_no=200),
            CheckItem(description='登录入口应具有防止暴力猜解及撞库猜解（利用已泄漏的密码字典进行尝试）的措施，超过设定失败次数需要启用锁定或CAPTCHA图片随机码', flow=task_flow,
                      product_type='GEN', sort_no=300),
            CheckItem(description='用户口令的主保护措施使用SHA256/SHA512/SHA-3或更高强度的散列算法，不使用MD5或SHA-1', flow=task_flow,
                      product_type='GEN', sort_no=400),
            CheckItem(description='交易/支付过程应形成完整的证据链，待交易数据应经过发起方数字签名', flow=task_flow, product_type='GEN', sort_no=500),
            CheckItem(description='软件升级/规则下发等数据分发过程，接收方应验证数据源的完整性(数字签名/HASH等)', flow=task_flow, product_type='GEN',
                      sort_no=600),
            CheckItem(description='设计上支持SOD( Seperation of Duty权限分离)，操作系统管理员、应用管理员、数据库管理员可以由不同的人员担任', flow=task_flow,
                      product_type='GEN', sort_no=700),
            CheckItem(description='软件发布前应经过数字签名', flow=task_flow, product_type='CLIENT', sort_no=100),
            CheckItem(description='启动时应对软件包所含的全部可执行文件、库、配置文件进行完整性校验，防止篡改或替换', flow=task_flow, product_type='CLIENT',
                      sort_no=200),
            CheckItem(description='客户端与服务器建立会话前应首先验证服务器证书的合法性，防止用户流量被劫持', flow=task_flow, product_type='CLIENT',
                      sort_no=300),
        ])
    return


def init_sec_dev_checklist():
    task_flow = TaskFlow.objects.get(type='SEC_DEV')
    if task_flow.flow_check_items.count() == 0:
        CheckItem.objects.bulk_create([
            CheckItem(description='前端不能直接访问数据库，应采取三层架构（表现层、业务逻辑层、数据访问层）', flow=task_flow, product_type='GEN',
                      sort_no=100),
            CheckItem(description='登录入口应具有防止暴力猜解及撞库猜解（利用已泄漏的密码字典进行尝试）的措施，超过设定失败次数需要启用锁定或CAPTCHA图片随机码', flow=task_flow,
                      product_type='GEN', sort_no=200),
            CheckItem(description='应不信任、不依赖客户端的安全控制措施，无论客户端采取何种措施，服务器侧都必须对用户提交的数据进行合法性检测', flow=task_flow,
                      product_type='GEN', sort_no=300),
            CheckItem(
                description='SQL语句应使用预编译和绑定变量的机制以实现SQL指令和参数的分离，不要拼接SQL语句，如有必须拼接的场景，应对每个参数进行合法性验证，包括整型验证、单引号的数据库转义(将单引号转换为两个单引号)等',
                flow=task_flow, product_type='GEN', sort_no=400),
            CheckItem(description='对需要输出到用户浏览器的任何由用户创造的内容，应在输出到浏览器之前或持久化存储之前进行转义(至少对<>转义为&lt; &gt;)以防止跨站攻击脚本(XSS)',
                      flow=task_flow, product_type='GEN', sort_no=500),
            CheckItem(
                description='针对交易或特权操作，应防止跨站请求伪造，应在框架层面为每个Form启用隐藏属性的CSRF Token，或者使用图片CAPTCHA由用户手工输入，或者使用支付口令等措施，修改密码须输入原密码，以防止跨站请求伪造(CSRF)',
                flow=task_flow, product_type='GEN', sort_no=600),
            CheckItem(description='应限定用户上传的附件类型，并对用户提交的图片/资源进行二次渲染(或添加水印/格式转换等)以破坏其原有结构，防止引入有害文件(网页木马等)',
                      flow=task_flow, product_type='GEN', sort_no=700),
            CheckItem(description='不使用路径或文件名作参数以防止目录遍历，不接受/不信任/不展示未经验证的外部图片或资源链接', flow=task_flow, product_type='GEN',
                      sort_no=800),
            CheckItem(description='用户口令的主保护措施使用SHA256/SHA512/SHA-3或更高强度的散列算法，不使用MD5或SHA-1', flow=task_flow,
                      product_type='GEN', sort_no=900),
            CheckItem(description='对敏感信息纪录做适当隐藏（如以星号代替部分信息），不发送/不展示完整的敏感信息，数据库应对敏感信息的部分字段进行加密，确保泄露之后不能构成完整的信息纪录',
                      flow=task_flow, product_type='GEN', sort_no=1000),
            CheckItem(description='交易/支付过程应形成完整的证据链，待交易数据应经过发起方数字签名', flow=task_flow, product_type='GEN', sort_no=1100),
            CheckItem(description='软件升级/规则下发等数据分发过程，接收方应验证数据源的完整性(数字签名/HASH等)', flow=task_flow, product_type='GEN',
                      sort_no=1200),
            CheckItem(description='如条件满足，建议使用代码审计工具对代码进行扫描，无高危缺陷视为通过', flow=task_flow, product_type='GEN',
                      sort_no=1300),
            CheckItem(description='软件开发工具均为直接从官方站点下载的正版软件，而不是从第三方站点所获取的', flow=task_flow, product_type='CLIENT',
                      sort_no=100),
            CheckItem(description='客户端软件所包含的开源组件均为安全稳定版本，并直接从官方站点下载，而不是从第三方站点获取', flow=task_flow, product_type='CLIENT',
                      sort_no=200),
            CheckItem(description='软件发布前应经过数字签名', flow=task_flow, product_type='CLIENT', sort_no=300),
            CheckItem(description='启动时应对软件包所含的全部可执行文件、库、配置文件进行完整性校验，防止篡改或替换', flow=task_flow, product_type='CLIENT',
                      sort_no=400),
            CheckItem(description='客户端与服务器建立会话前应首先验证服务器证书的合法性，防止用户流量被劫持', flow=task_flow, product_type='CLIENT',
                      sort_no=500),
        ])
    return


def init_sec_test_checklist():
    task_flow = TaskFlow.objects.get(type='SEC_TEST')
    if task_flow.flow_check_items.count() == 0:
        CheckItem.objects.bulk_create([
            CheckItem(description='测试用例应包含每个HTTP参数的SQL注入测试', flow=task_flow, product_type='GEN', sort_no=100),
            CheckItem(description='测试用例应包含每个HTTP参数的XSS测试', flow=task_flow, product_type='GEN', sort_no=200),
            CheckItem(description='测试用例应包含检测到文件包含(File Inclusion，使用HTTP参数传递文件路径或文件名)直接判定为不通过', flow=task_flow,
                      product_type='GEN', sort_no=300),
            CheckItem(description='测试用例应包含不同角色互相交换链接的权限测试，链接为对方无权访问的链接', flow=task_flow, product_type='GEN',
                      sort_no=400),
            CheckItem(description='如Web应用提供上传功能，测试用例应包含上传网页木马的测试', flow=task_flow, product_type='GEN', sort_no=500),
            CheckItem(description='测试用例应包含检测可能导致信息泄露的冗余备份文件，包括zip/tar/tar.gz等', flow=task_flow, product_type='GEN',
                      sort_no=600),
            CheckItem(description='如条件满足，建议使用漏洞扫描工具(如WebCruiser Web Vulnerability Scanner等)对测试环境进行扫描', flow=task_flow,
                      product_type='GEN', sort_no=700),
            CheckItem(description='软件发布前应经过数字签名', flow=task_flow, product_type='CLIENT', sort_no=100),
            CheckItem(description='启动时应对软件包所含的全部可执行文件、库、配置文件进行完整性校验，防止篡改或替换', flow=task_flow, product_type='CLIENT',
                      sort_no=200),
            CheckItem(description='客户端与服务器建立会话前应首先验证服务器证书的合法性，防止用户流量被劫持', flow=task_flow, product_type='CLIENT',
                      sort_no=300),
        ])
    return


def init_sec_deploy_checklist():
    task_flow = TaskFlow.objects.get(type='SEC_DEPLOY')
    if task_flow.flow_check_items.count() == 0:
        CheckItem.objects.bulk_create([
            CheckItem(description='应配置Web服务器(Apache/Nginx等)以静态方式展示用户上传的图片资源，禁止应用服务器(PHP/JSP/CGI等)动态展示用户上传的资源',
                      flow=task_flow, product_type='GEN', sort_no=100),
            CheckItem(description='禁止为后台服务器（数据库等）配置互联网IP地址，仅使用局域网地址', flow=task_flow, product_type='GEN', sort_no=200),
            CheckItem(description='禁止数据库端口直接向互联网开放', flow=task_flow, product_type='GEN', sort_no=300),
            CheckItem(description='应关闭不需要的服务/端口', flow=task_flow, product_type='GEN', sort_no=400),
            CheckItem(description='配置网站HTTPS证书或其它加密传输措施', flow=task_flow, product_type='GEN', sort_no=500),
            CheckItem(description='检查各中间件（Web服务器软件、框架、数据库等）版本，确认是安全/稳定版本', flow=task_flow, product_type='GEN',
                      sort_no=600),
            CheckItem(description='如已建立内部运维通道，禁止后台管理入口、运维及远程控制端口向互联网开放', flow=task_flow, product_type='GEN',
                      sort_no=700),
            CheckItem(description='禁止在应用中配置使用数据库超级账号，应为应用配置专用账号并授予合理的权限', flow=task_flow, product_type='GEN',
                      sort_no=800),
            CheckItem(description='回收修改操作系统账号、数据库账号，以及其它外部集成账号口令', flow=task_flow, product_type='GEN', sort_no=900),
            CheckItem(description='确认没有使用空口令、弱口令、通用口令(多处重复使用同一个口令)', flow=task_flow, product_type='GEN', sort_no=900),
            CheckItem(description='软件发布前应经过数字签名', flow=task_flow, product_type='CLIENT', sort_no=100),
        ])
    return


def init_acceptance_checklist():
    task_flow = TaskFlow.objects.get(type='ACCEPT')
    if task_flow.flow_check_items.count() == 0:
        CheckItem.objects.bulk_create([
            CheckItem(description='CMDB库维护完成，新增CI（配置项）已登记、对已有CI的变更已同步更新、过期CI已删除或标记为作废', flow=task_flow,
                      product_type='GEN', sort_no=100),
            CheckItem(description='针对产品的备份协议（备份）已签署或更新，含备份数据内容或文件目录、备份方式、备份频度、备份保留份数与清理机制', flow=task_flow,
                      product_type='GEN', sort_no=200),
            CheckItem(description='已基于备份协议执行数据备份', flow=task_flow, product_type='GEN', sort_no=300),
            CheckItem(description='已基于备份内容执行恢复演练，可以成功恢复', flow=task_flow, product_type='GEN', sort_no=400),
            CheckItem(description='已完成安全部署自检（回收账户口令/服务器安全配置等）', flow=task_flow, product_type='GEN', sort_no=500),
            CheckItem(description='已完成UAT测试', flow=task_flow, product_type='GEN', sort_no=600),
            CheckItem(description='已实施服务状态监控，定时检测服务状态并自动重启异常关闭的服务', flow=task_flow, product_type='GEN', sort_no=700),
        ])
    return


def init_req_confirm_checklist():
    task_flow = TaskFlow.objects.get(type='REQ_CONFIRM')
    if task_flow.flow_check_items.count() == 0:
        CheckItem.objects.bulk_create([
            CheckItem(description='需求应明确包含安全需求，除通用的安全基线外，还应有明确的安全需求针对业务上可能面临的较大的业务安全风险（如资金损失、交易事务一致性被破坏）',
                      flow=task_flow, product_type='GEN', sort_no=100),
            CheckItem(description='需求分析或需求规格应和业务代表确认，确保项目组和业务对需求的理解保持一致', flow=task_flow, product_type='GEN',
                      sort_no=200),
            CheckItem(description='需求应明确包含安全需求，除通用的安全基线外，还应有明确的安全需求针对业务上可能面临的较大的业务安全风险', flow=task_flow,
                      product_type='CLIENT', sort_no=100),
            CheckItem(description='需求分析或需求规格应和业务代表确认，确保项目组和业务对需求的理解保持一致', flow=task_flow, product_type='CLIENT',
                      sort_no=200),
        ])
    return


def init_bid_checklist():
    task_flow = TaskFlow.objects.get(type='BID')
    if task_flow.flow_check_items.count() == 0:
        CheckItem.objects.bulk_create([
            CheckItem(description='应基于需求匹配度、市场份额、知名度、技术实力、业界评价等要素筛选出供应商长清单', flow=task_flow, product_type='GEN',
                      sort_no=100),
            CheckItem(description='应明确供应商进入短清单的标准（由长清单到短清单）', flow=task_flow, product_type='GEN', sort_no=200),
            CheckItem(description='应明确最终选型评分的标准（由短清单到中标），明确技术分/商务分比重、淘汰条款、中标评定标准', flow=task_flow, product_type='GEN',
                      sort_no=300),
            CheckItem(description='评分标准应经过采购部门审核，警惕商务陷阱（如低价中标，高价维保）', flow=task_flow, product_type='GEN', sort_no=400),
            CheckItem(description='应向短清单中的供应商发出RFP(Request for Proposal)，并跟踪确认供应商是否已在截至日期前提交方案建议书', flow=task_flow,
                      product_type='GEN', sort_no=500),
            CheckItem(description='应在QA或项目管理办公室监督下，基于评分标准确定中标方', flow=task_flow, product_type='GEN', sort_no=600),
            CheckItem(description='应基于需求匹配度、市场份额、知名度、技术实力、业界评价等要素筛选出供应商长清单', flow=task_flow, product_type='CLIENT',
                      sort_no=100),
            CheckItem(description='应明确供应商进入短清单的标准（由长清单到短清单）', flow=task_flow, product_type='CLIENT', sort_no=200),
            CheckItem(description='应明确最终选型评分的标准（由短清单到中标），明确技术分/商务分比重、淘汰条款、中标评定标准', flow=task_flow,
                      product_type='CLIENT', sort_no=300),
            CheckItem(description='评分标准应经过采购部门审核，警惕商务陷阱（如低价中标，高价维保）', flow=task_flow, product_type='CLIENT',
                      sort_no=400),
            CheckItem(description='应向短清单中的供应商发出RFP(Request for Proposal)，并跟踪确认供应商是否已在截至日期前提交方案建议书', flow=task_flow,
                      product_type='CLIENT', sort_no=500),
            CheckItem(description='应在QA或项目管理办公室监督下，基于评分标准确定中标方', flow=task_flow, product_type='CLIENT', sort_no=600),
        ])
    return


def init_design_tr_checklist():
    task_flow = TaskFlow.objects.get(type='DESIGN_TR')
    if task_flow.flow_check_items.count() == 0:
        CheckItem.objects.bulk_create([
            CheckItem(description='方案设计所采用的架构、选用的框架和技术组合，符合业界最佳实践，且组织已具备或能够具备对相关框架、中间件的运维能力', flow=task_flow,
                      product_type='GEN', sort_no=100),
            CheckItem(description='功能模块基本涵盖业务需求、项目范围，项目目标预期可以达成', flow=task_flow, product_type='GEN', sort_no=200),
            CheckItem(description='架构上支持性能、容量上的扩展，如业务需要，支持异地多点或多实例部署', flow=task_flow, product_type='GEN', sort_no=300),
            CheckItem(description='集成关系（从其它系统获取数据）已明确得到相关数据源负责人的许可或授权', flow=task_flow, product_type='GEN',
                      sort_no=400),
            CheckItem(description='针对设计方案的安全自检已完成，无重大安全风险', flow=task_flow, product_type='GEN', sort_no=500),
            CheckItem(description='安全自检已完成，无重大安全风险', flow=task_flow, product_type='CLIENT', sort_no=100),
            CheckItem(description='功能模块基本涵盖业务需求、项目范围，项目目标预期可以达成', flow=task_flow, product_type='CLIENT', sort_no=200),
        ])
    return


def init_publish_tr_checklist():
    task_flow = TaskFlow.objects.get(type='PUBLISH_TR')
    if task_flow.flow_check_items.count() == 0:
        CheckItem.objects.bulk_create([
            CheckItem(description='如产品引进新技术，已向运维团队组织培训，完成对相关框架、中间件的运维技能转移', flow=task_flow, product_type='GEN',
                      sort_no=100),
            CheckItem(description='功能测试、性能测试已通过', flow=task_flow, product_type='GEN', sort_no=200),
            CheckItem(description='已完成并通过安全测试自检，无重大安全风险', flow=task_flow, product_type='GEN', sort_no=300),
            CheckItem(description='实施方案已就绪，相关产品手册已输出或更新', flow=task_flow, product_type='GEN', sort_no=400),
            CheckItem(description='产品发布/实施所需要的资源（机房、服务器、带宽、域名等）已准备就绪', flow=task_flow, product_type='GEN', sort_no=500),
            CheckItem(description='已完成并通过安全测试自检，无重大安全风险', flow=task_flow, product_type='CLIENT', sort_no=100),
            CheckItem(description='已通过签名检测', flow=task_flow, product_type='CLIENT', sort_no=200),
        ])
    return


def init_checklist():
    init_sec_design_checklist()
    init_sec_dev_checklist()
    init_sec_test_checklist()
    init_sec_deploy_checklist()
    init_acceptance_checklist()
    init_req_confirm_checklist()
    init_bid_checklist()
    init_design_tr_checklist()
    init_publish_tr_checklist()
    return


def get_user_by_task_role(current_task, role):
    if role == "TASK_LEADER":
        return current_task.leader
    elif role == "TASK_REVIEWER":
        return current_task.reviewer
    elif role == "NONE":
        return None
    elif current_task.project:
        return get_user_by_project_role(current_task.project, role)
    return current_task.leader


def handle_task_approval(current_task, current_handler, handle_option, trustee_id, handle_remarks):
    _trustee = None
    if handle_option.do == "TRANSFER":
        if trustee_id:
            _trustee = User.objects.get(id=trustee_id)
            current_task.current_handler = _trustee
    elif handle_option.do == "APPROVE":
        current_task.status = current_task.status.next_status
        current_task.current_handler = get_user_by_task_role(current_task, current_task.status.handler_role)
    elif handle_option.do == "RETURN":
        current_task.status = current_task.status.pre_status
        current_task.current_handler = get_user_by_task_role(current_task, current_task.status.handler_role)
    if current_task.status.ready_state == "DONE":
        current_task.done_time = datetime.datetime.now()
    if handle_option.do != "UPDATE":
        current_task.save()
    clear_task_cache_by_id(current_task.id)
    TaskApproval.objects.create(handler=current_handler, task=current_task, option=handle_option,
                                remarks=handle_remarks, trustee=_trustee)
    task_url = pmp.settings.SAAS_PORTAL + '/tasklist/' + str(current_task.id)
    msg_body = '我处理了任务【%s】 %s 补充意见：%s 链接: %s' % (current_task.name, handle_option.opinion, handle_remarks, task_url)
    send_circle_msg(current_handler, msg_body)
    if current_task.current_handler:
        if current_task.current_handler != current_handler:
            send_msg(current_handler, current_task.current_handler, msg_body)
    return


def init_checklist_for_task(_task):
    if _task.task_checkresults.count() == 0:
        check_items = _task.flow.flow_check_items.filter(product_type=_task.project.product_type).order_by('sort_no')
        check_result_list = []
        for item in check_items:
            check_result_list.append(CheckResult(task=_task, check_item=item, result='NONE'))
        CheckResult.objects.bulk_create(check_result_list)
    return


def create_kcp_tasks(_project):
    project_phases = _project.flow.projectphase_set.all()
    for project_phase in project_phases:
        kcp_flows = project_phase.kcp_flows.all()
        for kcp_flow in kcp_flows:
            _leader = get_user_by_project_role(_project, kcp_flow.first_status.handler_role)
            _reviewer_role = kcp_flow.flow_statuses.get(ready_state='REVIEW').handler_role
            _reviewer = get_user_by_project_role(_project, _reviewer_role)
            _task = Task.objects.create(name='KCP-执行' + kcp_flow.name,
                                        flow=kcp_flow,
                                        status=kcp_flow.first_status,
                                        team=_project.team,
                                        description=kcp_flow.description,
                                        leader=_leader,
                                        reviewer=_reviewer,
                                        current_handler=_leader,
                                        plan_mandays=1.0, project=_project, is_kcp=True, is_subtask=False,
                                        done_in_project_phase=project_phase)
            init_checklist_for_task(_task)
            TaskApproval.objects.create(task=_task, remarks="Create KCP",)
    return
