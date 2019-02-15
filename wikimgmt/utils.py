# coding=utf-8
from models import Wiki


def init_wiki_items():
    if Wiki.objects.count() == 0:
        Wiki.objects.bulk_create([
            Wiki(abbr='TEAM', expression='产品团队',
                 description='''产品团队(Product Team), 是以产品为单位，管理产品生命周期的一组人员。
                 备注：
                 本平台所提到的团队均指产品团队。
                 '''),
            Wiki(abbr='PM', expression='项目经理',
                 description='''项目经理(Project Manager), 是由组织委派，领导团队来实现项目目标的人。
                 备注：
                 不同的组织，会有不同的安排，担任项目经理的人员可能有：项目经理(Project Manager)、项目群经理(Program Manager)、产品经理、版本经理、产品技术主管、Scrum Master、开发Leader等；
                 请根据您所在组织的惯常做法进行安排。
                 '''),
            Wiki(abbr='ARCHITECT', expression='架构师',
                 description='''架构师(Architect), 是制定解决方案、切分产品功能模块、制定模块之间集成关系、搭建产品整体核心框架的人。
                 '''),
            Wiki(abbr='DEV_REP', expression='开发代表',
                 description='''开发代表(Development Representative), 负责开发/编码的主要程序设计人员或开发Leader。
                 '''),
            Wiki(abbr='TEST_REP', expression='测试代表',
                 description='''测试代表(Test Representative), 负责测试的主要测试人员或测试Leader。
                 '''),
            Wiki(abbr='SECURITY_REVIEWER', expression='安全评审员',
                 description='''安全评审员(Security Reviewer), 审核安全自检结果，进行综合安全风险评估的人。
                 建议由来自安全团队的专职网络安全人员担任，对项目组的自检结果进行审核（安全评审员不承担自检任务）；
                 没有专职安全人员的组织，可在产品团队内部，指定一名具有安全设计经验的人员兼职担任此角色，但尽量不要与产品安全代表相同。'''),
            Wiki(abbr='OP_REP', expression='产品运维代表',
                 description='''产品运维代表(Product Operation Representative), 承担产品的发布/实施/安全配置的人。
                    备注：运维代表来自运维/实施团队，承担具体的发布/实施任务。
                    '''),
            Wiki(abbr='QA', expression='质量保障人员',
                 description='''质量保障人员(Quality Assuarance, QA), 承担项目流程辅导、阶段切换审批等工作。
                 备注：
                 建议由来自项目管理办公室(PMO)的人员或者负责过程控制的人员担任；
                 本平台中，QA负责审核项目每个阶段的任务完成情况及执行阶段切换。
                 如果您所在组织中没有设立QA角色，可以配置成团队的Leader/负责人，由团队的Leader/负责人来执行流程审批。'''),
            Wiki(abbr='QC', expression='质量控制',
                 description='''质量控制代表(Quality Control, QC)。
                 本平台中QC负责对技术评审、同行评审等质量控制活动的意见进行审核。
                 '''),
            Wiki(abbr='MANDAY_COST', expression='平均人天成本',
                 description='''平均人天成本，即组织支出的平均每人每天的人力资源成本（含税前工资、保险、公积金、办公租金、物业、水电、员工福利等）。
                 备注：
                 平均人天成本，因所在地区、人员构成不同而有所不同；
                 如对资金、预算不敏感，保留默认值即可；
                 如需计入，可按照平均税后日薪的两倍进行估算，即：
                 平均人天成本 = 平均税后日薪 &times; 2
                 '''),
            Wiki(abbr='SPONSOR', expression='项目赞助人',
                 description='''项目赞助人(Sponsor)，为项目提供资源（人力、物力、预算）的人，通常为管理层具有决策权的人。
                 项目中的主要职责：为项目提供资源，决策立项，授权项目经理使用组织资源以达成项目目标，验收结果确认。
                 除精简项目管理流程不需要Sponsor参与决策外，其它项目管理流程需要Sponsor参与。
                 '''),
            Wiki(abbr='BUSINESS_REP', expression='业务代表',
                 description='''业务代表: 代表业务确认需求的人。
                 项目中的主要职责：审核项目需求分析，确保项目组与业务对需求的理解保持一致。
                 '''),
            Wiki(abbr='CHIEF_REVIEWER', expression='主审人',
                 description='''主审人：专家评审团（负责对方案设计的功能、性能、安全、集成、可维护性等进行把关）的第一负责人，技术评审活动中的决策者。
                 项目中的职责：技术评审活动中汇总各领域专家（含主审人自己）的意见，给出评审决策意见（通过/返回改进）。
                 '''),
            Wiki(abbr='PEER_REVIEWER', expression='同行评审代表',
                 description='''同行评审代表(Peer reviewer)：具有丰富经验的领域（行业）内专家或资深人士。
                 一般选择在公司内曾经做过类似项目的同事担任。
                 项目中的职责：评审产品方案设计，给出改进意见。
                 '''),
            Wiki(abbr='PURCHASING_REP', expression='采购代表',
                 description='''采购代表：由采购部门派出，对接本项目相关采购活动的采购人员。
                 项目中的职责：指导项目组遵循采购流程，受理采购需求。
                 如果项目不涉及采购，本角色填写项目经理自己即可。
                 '''),
            Wiki(abbr='USER_REP', expression='用户代表',
                 description='''用户代表：由员工担任，但以最终用户身份试用、体验待交付产品的人。
                 项目中的职责：以最终用户身份试用、体验待交付产品，对UAT测试结果进行确认。
                 '''),
            Wiki(abbr='STAKEHOLDER', expression='干系人',
                 description='''干系人(Stakeholder)：非项目成员，但跟项目有利益关系的人，需要知道项目的概况（主要是进展）。
                 项目的例行报告（周报/月报等）需抄送项目干系人。该角色可选（留空）。
                 '''),
            Wiki(abbr='HARDWARE_COST', expression='硬件预算',
                 description='''硬件预算：服务器、存储或其它设备的预算
                 '''),
            Wiki(abbr='SOFTWARE_COST', expression='软件预算',
                 description='''软件预算：采购软件包的一次性费用以及第一年License授权的费用
                 '''),
            Wiki(abbr='OTHER_COST', expression='其它费用',
                 description='''其它费用：除已列出的费用外，其它需要在项目中支出的费用。
                 '''),
            Wiki(abbr='ANNUAL_LICENSE_COST', expression='每年License费用',
                 description='''每年License费用：预估每年用于采购License的支出。不属于项目内预算，但属于运维成本，供决策参考。
                 '''),
            Wiki(abbr='ANNUAL_OTHER_COST', expression='每年其它费用',
                 description='''每年其它费用：除License外，预估的每年例行支出（硬件维保等），不属于项目内预算，属于运维成本，供决策参考
                 '''),
        ])
    return
