# coding=utf-8
from django.db import models
from usermgmt.models import User, Company


# Config Management
class AppType(models.Model):
    name=models.CharField(max_length=128, unique=True) # Web, Web_Service

    def __unicode__(self):
        return self.name


class MiddleWareType(models.Model):
    name=models.CharField(max_length=128, unique=True) # NGINX, MySQL, django

    def __unicode__(self):
        return self.name


class DatabaseType(models.Model):
    name=models.CharField(max_length=128, unique=True) # MySQL, SQLite

    def __unicode__(self):
        return self.name


class OsType(models.Model):
    name=models.CharField(max_length=128, unique=True) # CentOS, Redhat, Windows

    def __unicode__(self):
        return self.name


class ServerType(models.Model):
    name=models.CharField(max_length=128, unique=True) # Cloud Server, VPS, Dedicated Server

    def __unicode__(self):
        return self.name


class StorageType(models.Model):
    name=models.CharField(max_length=128, unique=True) #

    def __unicode__(self):
        return self.name


class NetworkDeviceType(models.Model):
    name=models.CharField(max_length=128, unique=True) #

    def __unicode__(self):
        return self.name


CI_CATEGORY_CHOICES = (
    ('APP', '产品/应用/服务'),
    ('CLUSTER', '集群/虚拟节点'),
    ('DB', '数据库'),
    ('MIDDLEWARE', '中间件'),
    ('SERVICE', '系统服务'),
    ('OS', '操作系统'),
    ('SERVER', '服务器'),
    ('STORAGE', '存储设备'),
    ('NETDEV', '网络设备'),
    ('ROOM', '机房'),
    ('OTHER', '其它'),
)

CI_STATUS_CHOICES = (
    ('ONLINE', '正常/有效'),
    ('OFFLINE', '冷备/未启用'),
    ('READY', '就绪/准备上线'),
    ('EXPIRE', '已停止维护/准备下线'),
    ('INVALID', '已作废'),
)

IP_CATEGORY_CHOICES = (
    ('INNER','内网业务IP地址'),
    ('OUTER','外网业务IP地址'),
    ('DMZ','DMZ业务IP地址'),
    ('ADM','管理网IP地址'),
    ('BAK','备份网IP地址'),
    ('VPN','专网IP地址'),
    ('OTHER','其它IP地址'),
)


class IP(models.Model):
    name=models.GenericIPAddressField()
    category=models.CharField(max_length=32, choices=IP_CATEGORY_CHOICES, default='OUTER')
    company=models.ForeignKey(Company, related_name='company_ips')

    def __unicode__(self):
        return self.name


class Domain(models.Model):
    name=models.CharField(max_length=128, unique=True)
    ip=models.ForeignKey(IP, blank=True, null=True, related_name='ip_domains')
    company=models.ForeignKey(Company, related_name='company_domains')

    def __unicode__(self):
        return self.name


class CI(models.Model):
    name=models.CharField(max_length=128)
    category=models.CharField(max_length=32, choices=CI_CATEGORY_CHOICES)
    description=models.CharField(max_length=256, blank=True, null=True)
    company=models.ForeignKey(Company, related_name='company_cis')
    create_time=models.DateTimeField(auto_now_add=True)
    admins=models.ManyToManyField(User, blank=True)
    status=models.CharField(max_length=32, choices=CI_STATUS_CHOICES, default='ONLINE')
    bind_domains=models.ManyToManyField(Domain, blank=True,related_name='domain_cis')
    bind_ips=models.ManyToManyField(IP, blank=True, related_name='ip_cis')
    ports=models.CharField(max_length=128, blank=True, null=True)
    down_stream_cis=models.ManyToManyField('self', blank=True, related_name='up_stream_cis', symmetrical=False)
    integrations=models.ManyToManyField('self', through='IntegrationRelation', symmetrical=False)
    # use multi-table inheritance

    def __unicode__(self):
        return self.name


class IntegrationRelation(models.Model):
    source=models.ForeignKey(CI, related_name='source_relations')
    destination=models.ForeignKey(CI, related_name='destination_relations')
    source_label=models.CharField(max_length=64, blank=True, null=True)
    destination_label=models.CharField(max_length=64, blank=True, null=True)


class ROOM(CI):
    city=models.CharField(max_length=64)
    address=models.CharField(max_length=128, blank=True, null=True)
    contact=models.CharField(max_length=128, blank=True, null=True)


class STORAGE(CI):
    type=models.ForeignKey(StorageType)
    model=models.CharField(max_length=128, blank=True, null=True)
    admin_portal=models.CharField(max_length=128, blank=True, null=True)


class NETDEV(CI):
    type=models.ForeignKey(NetworkDeviceType)
    model=models.CharField(max_length=128, blank=True, null=True)
    admin_portal=models.CharField(max_length=128, blank=True, null=True)


class SERVER(CI):
    type=models.ForeignKey(ServerType, blank=True, null=True)
    model=models.CharField(max_length=128, blank=True, null=True)
    admin_portal=models.CharField(max_length=128, blank=True, null=True)


class OS(CI):
    type=models.ForeignKey(OsType)
    os_name=models.CharField(max_length=64)
    version=models.CharField(max_length=64, blank=True, null=True)


class MIDDLEWARE(CI):
    type=models.ForeignKey(MiddleWareType)
    middleware_name=models.CharField(max_length=64)
    version=models.CharField(max_length=64, blank=True, null=True)


class DB(CI):
    type=models.ForeignKey(DatabaseType)
    version=models.CharField(max_length=64, blank=True, null=True)


class SERVICE(CI):
    service_name=models.CharField(max_length=128)


class APP(CI):
    type=models.ForeignKey(AppType)
    version=models.CharField(max_length=64, blank=True, null=True)
    user_portal=models.CharField(max_length=128, blank=True, null=True)
    admin_portal=models.CharField(max_length=128, blank=True, null=True)
