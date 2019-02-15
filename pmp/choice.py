# coding=utf-8

PRODUCT_TYPE_CHOICES = (
    ('GEN', '通用Web应用或C/S架构产品，强化服务器侧安全'),
    ('CLIENT', 'PC或移动客户端应用，强化终端安全'),
    ('OTHER', '其它'),
)

CHECK_RESULT_CHOICES = (
    ('NONE', '未检查'),
    ('YES', '符合'),
    ('NO', '不符合'),
    ('NA', '不涉及'),
)

CUSTOM_CHECK_RESULT_CHOICES = (
    ('NONE', '未完成'),
    ('YES', '完成(OK)'),
    ('NO', '无法完成(放弃)'),
    ('NA', '不涉及(作废)'),
)

PROJECT_FLOW_TYPE_CHOICES = (
    ('AGL', '精简安全内控项目管理流程'),  # Agile
    ('APP', '应用开发安全内控项目管理流程'),  # Application
    ('INF', '外购软件包实施安全内控项目管理流程'),  # Infrastructure
    ('CUS', '自定义项目管理流程'),
)

PROJECT_PHASE_READY_STATES = (
    ('PLAN', '规划中'),
    ('PROCESS', '进行中'),
    ('CLOSE', '已结束'),
)

TASK_READY_STATES =(
    ('TODO', '待执行'),
    ('PROCESSING', '执行中'),
    ('REVIEW', '复核中'),
    ('DONE', '已完成'),
)

PROJECT_STATUS_CHOICES = (
    ('IN_PROCESS', '进行中'),
    ('IN_APPROVAL', '审批中'),
    ('IN_OPERATION', '已结束'),
)


FLOW_APPROVAL_CHOICES = (
    ('SUBMIT', '提交审核'),
    ('APPROVE', '同意'),
    ('RETURN', '返回'),
    ('TRANSFER', '转他人处理'),
    ('UPDATE', '备注/更新进度说明'),
)

ROLE_CHOICES = (
    ('PM', '项目经理'),
    ('ARCHITECT', '架构师/方案设计师'),
    ('DEV_REP', '开发代表'),
    ('TEST_REP', '测试代表'),
    ('OP_REP', '运维代表'),
    ('SECURITY_REVIEWER', '安全审核员'),
    ('SPONSOR', 'Sponsor(赞助人/人力及预算决策人)'),
    ('CHIEF_REVIEWER', '主审人(技术评审组组长)'),
    ('PEER_REVIEWER', '同行评审(专家代表)'),
    ('BUSINESS_REP', '业务代表(需求审核确认)'),
    ('PURCHASING_REP', '采购代表(招标/选型结果确认)'),
    ('USER_REP', '用户代表(UAT测试结果确认)'),
    ('QA', 'QA质量保障'),
    ('QC', 'QC质量控制'),
    ('TASK_LEADER', '任务负责人'),
    ('TASK_REVIEWER', '任务复核人'),
    ('NONE', '不需要处理'),
)

# Default Task flows

TASK_FLOW_TYPE_CHOICES = (
    ('GEN', '通用工作流'),
    ('SEC_DESIGN', '安全设计自检工作流'),
    ('SEC_DEV', '安全开发自检工作流'),
    ('SEC_TEST', '安全测试自检工作流'),
    ('SEC_DEPLOY', '安全部署自检工作流'),
    ('ACCEPT', '验收工作流'),
    ('REQ_CONFIRM', '需求确认工作流'),
    ('BID', '选型工作流'),
    ('DESIGN_TR', '方案设计评审自检工作流'),
    ('PUBLISH_TR', '上线发布评审自检工作流'),
    ('SEC_TEST', '安全测试工作流'),
    ('SEC_CFG', '安全配置工作流'),
    ('BACKUP', '备份工作流'),
    ('CUS', '自定义工作流'),
    ('TEAMWORK', '协作工作流'),
)
