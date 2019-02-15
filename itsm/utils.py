# coding=utf-8
from models import *
import json
from django.apps import apps


def init_demo_cis():
    if AppType.objects.count()==0:
        AppType.objects.bulk_create([
            AppType(name='Web动态业务应用'),
            AppType(name='Web静态业务网站'),
            AppType(name='基于WebService的动态业务应用'),
            AppType(name='基于Socket的业务应用'),
            AppType(name='IT基础设施服务'),
            AppType(name='软硬一体化系统'),
            AppType(name='其它应用'),
        ])
    if MiddleWareType.objects.count()==0:
        MiddleWareType.objects.bulk_create([
            MiddleWareType(name='Web服务器组件(Apache/Nginx/IIS等)'),
            MiddleWareType(name='应用服务器组件(CGI/PHP-FPM/Tomcat等)'),
            MiddleWareType(name='应用框架组件(Struts/Django/ThinkPHP等)'),
            MiddleWareType(name='消息组件(MQ)'),
            MiddleWareType(name='缓存组件(Memcached/Redis等)'),
            MiddleWareType(name='总线组件(BUS)'),
            MiddleWareType(name='第三方服务组件(CDN/云WAF等)'),
            MiddleWareType(name='其它组件'),
        ])
    if DatabaseType.objects.count()==0:
        DatabaseType.objects.bulk_create([
            DatabaseType(name='MySQL'),
            DatabaseType(name='SQLite'),
            DatabaseType(name='PostgreSQL'),
            DatabaseType(name='SQLServer'),
            DatabaseType(name='Oracle'),
            DatabaseType(name='DB2'),
            DatabaseType(name='Informix'),
            DatabaseType(name='Sybase'),
            DatabaseType(name='Access'),
            DatabaseType(name='Redis'),
            DatabaseType(name='MongoDB'),
            DatabaseType(name='Cassandra'),
            DatabaseType(name='HBase'),
            DatabaseType(name='SequoiaDB'),
            DatabaseType(name='其它数据库类型'),
        ])
    if OsType.objects.count()==0:
        OsType.objects.bulk_create([
            OsType(name='Linux(CentOS/Debian/Redhat等)'),
            OsType(name='UNIX(BSD/AIX/Solaris/UX等)'),
            OsType(name='Windows(2003/2008等)'),
            OsType(name='其它系统'),
        ])
    if ServerType.objects.count()==0:
        ServerType.objects.bulk_create([
            ServerType(name='云服务器(Cloud Server)'),
            ServerType(name='VPS(Virtual Private Server)'),
            ServerType(name='独立服务器(Dedicated Server)'),
            ServerType(name='其它(Other)'),
        ])
    if NetworkDeviceType.objects.count()==0:
        NetworkDeviceType.objects.bulk_create([
            NetworkDeviceType(name='路由交换设备(路由器/交换机等)'),
            NetworkDeviceType(name='安全设备(IPS/防火墙/审计等)'),
            NetworkDeviceType(name='其它设备'),
        ])
    if StorageType.objects.count()==0:
        StorageType.objects.bulk_create([
            StorageType(name='NAS(Network Attached Storage)'),
            StorageType(name='SAN(Storage Area Network)'),
            StorageType(name='DAS(Direct Attach Storage)'),
            StorageType(name='其它存储'),
        ])
    if CI.objects.count()==0:
        _company=Company.objects.get(top_domain_name='janusec.com')
        _room=ROOM.objects.create(name='JAN-ROOM-001', category='ROOM', company=_company, city='深圳')
        _server_type=ServerType.objects.get(name__icontains='独立服务器')
        _server001=SERVER.objects.create(name='JAN-SERVER-001', category='SERVER', company=_company, type=_server_type)
        _os_type=OsType.objects.get(name__icontains='Linux')
        _os001=OS.objects.create(name='JAN-CENTOS-001', category='OS', type=_os_type, company=_company, os_name='CentOS', version='6.5')
        _os002=OS.objects.create(name='JAN-CENTOS-002', category='OS', type=_os_type, company=_company, os_name='CentOS', version='6.4')
        _db_type=DatabaseType.objects.get(name='MySQL')
        _db001=DB.objects.create(name='JAN-MYSQL-001', category='DB', type=_db_type, company=_company, version='5.6')
        _mid_type=MiddleWareType.objects.get(name__icontains='Nginx')
        _mid001=MIDDLEWARE.objects.create(name='JAN-NGINX-001', category='MIDDLEWARE', type=_mid_type, company=_company, middleware_name='Nginx', version='1.6.2')
        _app_type=AppType.objects.get(name__icontains='Web动态业务应用')
        app=APP.objects.create(name='JAN-APP-PMP', category='APP', type=_app_type, company=_company)
        _server001.down_stream_cis.add(_room)
        _server001.save()
        _os001.down_stream_cis.add(_server001)
        _os002.down_stream_cis.add(_server001)
        _os001.save()
        _os002.save()
        _mid001.down_stream_cis.add(_os001)
        _mid001.save()
        _db001.down_stream_cis.add(_os002)
        _db001.save()
        app.down_stream_cis.add(_mid001)
        app.down_stream_cis.add(_db001)
        app.save()
    return


def get_ci_dict(ci):
    ci_dict={}
    ci_dict['id']=ci.id
    ci_dict['name']=ci.name
    ci_dict['category']=ci.get_category_display()
    ci_dict['description']=ci.description
    return ci_dict


def get_ci_stream_dict(ci):
    ci_dict=get_ci_dict(ci)
    up_stream_list=[]
    for up_ci in ci.up_stream_cis.all():
        up_stream_list.append(get_ci_dict(up_ci))
    ci_dict['up_stream_cis']=up_stream_list
    down_stream_list=[]
    for down_ci in ci.down_stream_cis.all():
        down_stream_list.append(get_ci_dict(down_ci))
    ci_dict['down_stream_cis']=down_stream_list
    return ci_dict


def get_ci_stream_json(ci):
    ci_dict=get_ci_stream_dict(ci)
    return json.dumps(ci_dict, ensure_ascii=False)


def get_ci_by_id(ci_id):
    try:
        ci=CI.objects.get(id=ci_id)
    except:
        return (None,None)
    try:
        sub_model=apps.get_model('itsm',ci.category)
    except:
        return (ci,None)
    sub_ci=sub_model.objects.get(id=ci_id)
    sub_ci_dict={}
    for field in sub_ci._meta.get_fields(include_parents=False, include_hidden=False):
        if field.name!='ci_ptr':
            value=getattr(sub_ci, field.name, None)
            if not value or isinstance(value, unicode):
                sub_ci_dict[field.name]=value
            elif value.__class__.__name__=='ManyRelatedManager':
                list_str=""
                for item in value.all():
                    if list_str:
                        list_str+=", "
                    list_str+=item.name
                sub_ci_dict[field.name]=list_str
            else:
                sub_ci_dict[field.name]=value.name
    return (sub_ci,sub_ci_dict)


def permit_delete_ip(_user, ip):
    if _user.company != ip.company:
        return False
    if ip.ip_domains.count()>0:
        return False
    if ip.ip_cis.count()>0:
        return False
    return True


def permit_delete_domain(_user, domain):
    if _user.company != domain.company:
        return False
    if domain.domain_cis.count()>0:
        return False
    return True


def get_additional_fields_list_by_category(category):
    additional_fields=[]
    if category=="APP":
        additional_fields.append({"name":"version", "verbose_name":"产品/应用版本", "options":""})
        additional_fields.append({"name":"user_portal", "verbose_name":"用户访问入口", "options":""})
        additional_fields.append({"name":"admin_portal", "verbose_name":"后台管理入口", "options":""})
    elif category=="CLUSTER":
        pass
    elif category=="DB":
        options=[]
        for item in DatabaseType.objects.order_by("id"):
            options.append({"id":item.id, "description":item.name})
        additional_fields.append({"name":"type", "verbose_name":"数据库类型", "options":options})
        additional_fields.append({"name":"version", "verbose_name":"数据库版本", "options":""})
    elif category=="MIDDLEWARE":
        options=[]
        for item in MiddleWareType.objects.order_by("id"):
            options.append({"id":item.id, "description":item.name})
        additional_fields.append({"name":"type", "verbose_name":"中间件类型", "options":options})
        additional_fields.append({"name":"middleware_name", "verbose_name":"中间件名称", "options":""})
        additional_fields.append({"name":"version", "verbose_name":"中间件版本", "options":""})
    elif category=="SERVICE":
        additional_fields.append({"name":"service_name", "verbose_name":"系统服务名称", "options":""})
    elif category=="OS":
        options=[]
        for item in OsType.objects.order_by("id"):
            options.append({"id":item.id, "description":item.name})
        additional_fields.append({"name":"type", "verbose_name":"操作系统类型", "options":options})
        additional_fields.append({"name":"os_name", "verbose_name":"操作系统名称", "options":""})
        additional_fields.append({"name":"version", "verbose_name":"操作系统版本", "options":""})
    elif category=="SERVER":
        options=[]
        for item in ServerType.objects.order_by("id"):
            options.append({"id":item.id, "description":item.name})
        additional_fields.append({"name":"type", "verbose_name":"服务器类型", "options":options})
        additional_fields.append({"name":"model", "verbose_name":"硬件型号", "options":""})
        additional_fields.append({"name":"admin_portal", "verbose_name":"管理地址", "options":""})
    elif category=="STORAGE":
        options=[]
        for item in StorageType.objects.order_by("id"):
            options.append({"id":item.id, "description":item.name})
        additional_fields.append({"name":"type", "verbose_name":"存储类型", "options":options})
        additional_fields.append({"name":"model", "verbose_name":"硬件型号", "options":""})
        additional_fields.append({"name":"admin_portal", "verbose_name":"管理地址", "options":""})
    elif category=="NETDEV":
        options=[]
        for item in NetworkDeviceType.objects.order_by("id"):
            options.append({"id":item.id, "description":item.name})
        additional_fields.append({"name":"type", "verbose_name":"设备类型", "options":options})
        additional_fields.append({"name":"model", "verbose_name":"设备型号", "options":""})
        additional_fields.append({"name":"admin_portal", "verbose_name":"管理地址", "options":""})
    elif category=="ROOM":
        additional_fields.append({"name":"city", "verbose_name":"城市（必填）", "options":""})
        additional_fields.append({"name":"address", "verbose_name":"具体地址", "options":""})
        additional_fields.append({"name":"contact", "verbose_name":"联系方式", "options":""})
    return additional_fields
