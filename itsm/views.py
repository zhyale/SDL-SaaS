# coding=utf-8
from django.shortcuts import render
from models import *
from usermgmt.utils import get_valid_user
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from utils import get_ci_stream_json, get_ci_by_id, permit_delete_ip, permit_delete_domain, get_additional_fields_list_by_category
from cache import get_ci_set, get_all_ip, get_all_domain


def itsm(request):
    _user = get_valid_user(request)
    return render(request, 'itsm.html', {'current_user': _user})


def configuration_management(request):
    _user = get_valid_user(request)
    if not _user:
        return HttpResponseRedirect('/login')
    if request.method=="GET":
        ci_set=get_ci_set(_user)
        return render(request, 'itsm_config.html', {'current_user': _user, 'ci_set':ci_set, 'categories':CI_CATEGORY_CHOICES})
    keyword=request.POST.get("s","")
    result_cis=None
    if keyword:
        result_cis=CI.objects.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword) , company=_user.company)
        if not result_cis:
            messages.add_message(request, messages.INFO, ('未找到相应的配置项(CI) !'))
    ci_set=None
    if not result_cis:
        ci_set=get_ci_set(_user)
    return render(request, 'itsm_config.html', {'current_user': _user, 'result_cis':result_cis, 'ci_set':ci_set, 'categories':CI_CATEGORY_CHOICES})


def get_category_display(category):
    for value, display in CI_CATEGORY_CHOICES:
        if category==value:
            return display
    return '其它'


def ci_operation(request, op):
    _user = get_valid_user(request)
    if not _user:
        return HttpResponseRedirect('/login')
    if request.method!="POST":
        return HttpResponseRedirect('/itsm/configuration-management')
    if op=="add":
        _category=request.POST.get("category","OTHER")
        additional_fields=get_additional_fields_list_by_category(_category)
        return render(request, 'itsm_ci_create.html', {'current_user': _user, 'category':_category,
                                                       'category_display':get_category_display(_category),
                                                       'status_choices':CI_STATUS_CHOICES,
                                                       'additional_fields':additional_fields})
    elif op=="create":
        _name=request.POST.get("name",None)
        if not _name:
            messages.add_message(request, messages.INFO, ('CI Name不能为空!'))
            return HttpResponseRedirect('/itsm/configuration-management')
        try:
            CI.objects.get(company=_user.company, name=_name)
            messages.add_message(request, messages.INFO, ('CI名称已存在，请重新设置CI名称!'))
            return HttpResponseRedirect('/itsm/configuration-management')
        except:
            pass
        _category=request.POST.get("category","OTHER")
        _description=request.POST.get("description","")
        _status=request.POST.get("status","ONLINE")
        _ports=request.POST.get("ports","")
        _ci=None
        if _category=="APP":
            _version=request.POST.get("version","")
            _user_portal=request.POST.get("user_portal","")
            _admin_portal=request.POST.get("admin_portal","")
            _ci=APP.objects.create(name=_name, category=_category, description=_description, company=_user.company, status=_status, ports=_ports,
                               version=_version, user_portal=_user_portal, admin_portal=_admin_portal)
        elif _category=="CLUSTER":
            _ci=CI.objects.create(name=_name, category=_category, description=_description, company=_user.company, status=_status, ports=_ports)
        elif _category=="DB":
            _id=request.POST.get("type",1)
            _type=DatabaseType.objects.get(id=_id)
            _version=request.POST.get("version","")
            _ci=DB.objects.create(name=_name, category=_category, description=_description, company=_user.company, status=_status, ports=_ports,
                              type=_type, version=_version)
        elif _category=="MIDDLEWARE":
            _id=request.POST.get("type",1)
            _type=MiddleWareType.objects.get(id=_id)
            _middleware_name=request.POST.get("middleware_name","")
            _version=request.POST.get("version","")
            _ci=MIDDLEWARE.objects.create(name=_name, category=_category, description=_description, company=_user.company, status=_status, ports=_ports,
                              type=_type,middleware_name=_middleware_name, version=_version)
        elif _category=="SERVICE":
            _service_name=request.POST.get("service_name","")
            _ci=SERVICE.objects.create(name=_name, category=_category, description=_description, company=_user.company, status=_status, ports=_ports,
                                   service_name=_service_name)
        elif _category=="OS":
            _id=request.POST.get("type",1)
            _type=OsType.objects.get(id=_id)
            _os_name=request.POST.get("os_name","")
            _version=request.POST.get("version","")
            _ci=OS.objects.create(name=_name, category=_category, description=_description, company=_user.company, status=_status, ports=_ports,
                              type=_type, os_name=_os_name, version=_version)
        elif _category=="SERVER":
            _id=request.POST.get("type",1)
            _type=ServerType.objects.get(id=_id)
            _model=request.POST.get("model","")
            _admin_portal=request.POST.get("admin_portal","")
            _ci=SERVER.objects.create(name=_name, category=_category, description=_description, company=_user.company, status=_status, ports=_ports,
                              type=_type, model=_model, admin_portal=_admin_portal)
        elif _category=="STORAGE":
            _id=request.POST.get("type",1)
            _type=StorageType.objects.get(id=_id)
            _model=request.POST.get("model","")
            _admin_portal=request.POST.get("admin_portal","")
            _ci=STORAGE.objects.create(name=_name, category=_category, description=_description, company=_user.company, status=_status, ports=_ports,
                              type=_type, model=_model, admin_portal=_admin_portal)
        elif _category=="NETDEV":
            _id=request.POST.get("type",1)
            _type=NetworkDeviceType.objects.get(id=_id)
            _model=request.POST.get("model","")
            _admin_portal=request.POST.get("admin_portal","")
            _ci=NETDEV.objects.create(name=_name, category=_category, description=_description, company=_user.company, status=_status, ports=_ports,
                              type=_type, model=_model, admin_portal=_admin_portal)
        elif _category=="ROOM":
            _city=request.POST.get("city","China")
            _address=request.POST.get("address","")
            _contact=request.POST.get("contact","")
            _ci=ROOM.objects.create(name=_name, category=_category, description=_description, company=_user.company, status=_status, ports=_ports,
                              city=_city, address=_address, contact=_contact)
        else:
            _ci=CI.objects.create(name=_name, category=_category, description=_description, company=_user.company, status=_status, ports=_ports)
        if _ci:
            _ci.admins.add(_user)
            _domains=request.POST.get("domains","")
            _ips=request.POST.get("ips","")
            bind_domains_to_ci(_ci, _domains, _user)
            bind_ips_to_ci(_ci, _ips, _user)
            _ci.save()
            messages.add_message(request, messages.INFO, ('配置项(CI) '+ _name + ' 创建成功 !'))
    elif op=="adddownci":
        current_id=request.POST.get("id","")
        current_ci=CI.objects.get(id=current_id)
        down_ci_name=request.POST.get("down_ci_name","")
        try:
            down_ci=CI.objects.get(name=down_ci_name)
            current_ci.down_stream_cis.add(down_ci)
            current_ci.save()
        except:
            messages.add_message(request, messages.INFO, ('您输入的CI不存在 !'))
        return HttpResponseRedirect('/itsm/ci/'+current_id)
    elif op=="addupci":
        current_id=request.POST.get("id","")
        current_ci=CI.objects.get(id=current_id)
        up_ci_name=request.POST.get("up_ci_name","")
        try:
            up_ci=CI.objects.get(name=up_ci_name)
            up_ci.down_stream_cis.add(current_ci)
            up_ci.save()
        except:
            messages.add_message(request, messages.INFO, ('您输入的CI不存在 !'))
        return HttpResponseRedirect('/itsm/ci/'+current_id)

    return HttpResponseRedirect('/itsm/configuration-management')


def bind_domains_to_ci(ci, domains, _user):
    domain_list=domains.split()
    for domain_name in domain_list:
        try:
            _domain=Domain.objects.get(name=domain_name)
        except:
            _domain=Domain.objects.create(name=domain_name, company=_user.company)
        ci.bind_domains.add(_domain)
    return


def bind_ips_to_ci(ci, ips, _user):
    ip_list=ips.split()
    for ip_address in ip_list:
        try:
            _ip=IP.objects.get(name=ip_address)
        except:
            _ip=IP.objects.create(name=ip_address, company=_user.company)
        ci.bind_ips.add(_ip)
    return


def show_ci(request, ci_id):
    _user = get_valid_user(request)
    if not _user:
        return HttpResponseRedirect('/login')
    (ci, sub_ci_dict)=get_ci_by_id(ci_id)
    if not ci:
        messages.add_message(request, messages.INFO, ('未找到相应的配置项(CI) !'))
        return HttpResponseRedirect('/itsm/configuration-management')
    ci_stream_json=get_ci_stream_json(ci)
    return render(request, 'itsm_showci.html', {'current_user': _user, 'ci':ci, 'ci_stream_json':ci_stream_json,'sub_ci_dict':sub_ci_dict})


def ip_management(request):
    _user = get_valid_user(request)
    if not _user:
        return HttpResponseRedirect('/login')
    if request.method=='GET':
        ips=get_all_ip(_user, False)
        return render(request, 'itsm_ip_mgmt.html', {'current_user': _user, 'ips':ips})
    do=request.POST.get("do","")
    if do=="search":
        keyword=request.POST.get("s","")
        result_ips=None
        if keyword:
            result_ips=IP.objects.filter(company=_user.company, name__contains=keyword)
            if not result_ips:
                messages.add_message(request, messages.INFO, ('未找到相应的IP !'))
        ips=None
        if not result_ips:
            ips=get_all_ip(_user, False)
        return render(request, 'itsm_ip_mgmt.html', {'current_user': _user, 'result_ips':result_ips, 'ips':ips})
    elif do=="add":
        _name=request.POST.get("name","")
        _category=request.POST.get("category","OUTER")
        try:
            IP.objects.create(name=_name, category=_category, company=_user.company)
        except:
            messages.add_message(request, messages.INFO, ('IP地址格式错误 !'))
        ips=get_all_ip(_user, True)
        return render(request, 'itsm_ip_mgmt.html', {'current_user': _user, 'ips':ips})
    elif do=="delete":
        _id=request.POST.get("id","")
        try:
            ip=IP.objects.get(id=_id)
            if permit_delete_ip(_user, ip):
                ip.delete()
                messages.add_message(request, messages.INFO, ('IP地址: '+ ip.name +'已删除 !'))
            else:
                messages.add_message(request, messages.INFO, ('您无权删除该IP地址 !'))
        except:
            messages.add_message(request, messages.INFO, ('IP地址不存在 !'))
    ips=get_all_ip(_user, False)
    return render(request, 'itsm_ip_mgmt.html', {'current_user': _user, 'ips':ips})


def domain_management(request):
    _user = get_valid_user(request)
    if not _user:
        return HttpResponseRedirect('/login')
    if request.method=='GET':
        domains=get_all_domain(_user, False)
        return render(request, 'itsm_domain_mgmt.html', {'current_user': _user, 'domains':domains})
    do=request.POST.get("do","")
    if do=="search":
        keyword=request.POST.get("s","")
        result_domains=None
        if keyword:
            result_domains=Domain.objects.filter(company=_user.company, name__contains=keyword)
            if not result_domains:
                messages.add_message(request, messages.INFO, ('未找到相应的域名 !'))
        domains=None
        if not result_domains:
            domains=get_all_domain(_user, False)
        return render(request, 'itsm_domain_mgmt.html', {'current_user': _user, 'result_domains':result_domains, 'domains':domains})
    elif do=="add":
        _name=request.POST.get("name","")
        ip_str=request.POST.get("ip","")
        _ip=None
        if ip_str:
            try:
                _ip=IP.objects.get(name=ip_str)
            except:
                _category=request.POST.get("category","OUTER")
                _ip=IP.objects.create(name=ip_str, category=_category, company=_user.company)
        Domain.objects.create(name=_name, ip=_ip, company=_user.company)
        domains=get_all_domain(_user, True)
        return render(request, 'itsm_domain_mgmt.html', {'current_user': _user, 'domains':domains})
    elif do=="delete":
        _id=request.POST.get("id","")
        try:
            domain=Domain.objects.get(id=_id)
            if permit_delete_domain(_user, domain):
                domain.delete()
                messages.add_message(request, messages.INFO, ('域名: '+ domain.name +'已删除 !'))
            else:
                messages.add_message(request, messages.INFO, ('您无权删除该域名 !'))
        except:
            messages.add_message(request, messages.INFO, ('域名不存在 !'))
    domains=get_all_domain(_user, False)
    return render(request, 'itsm_domain_mgmt.html', {'current_user': _user, 'domains':domains})


def show_ip(request, ip_id):
    _user = get_valid_user(request)
    if not _user:
        return HttpResponseRedirect('/login')
    try:
        ip=IP.objects.get(id=ip_id)
    except:
        messages.add_message(request, messages.INFO, ('未找到此IP !'))
        return HttpResponseRedirect('/itsm/ip-management')
    permit_delete=permit_delete_ip(_user, ip)
    return render(request, 'itsm_ipinfo.html', {'ip':ip, 'permit_delete':permit_delete})


def show_domain(request, domain_id):
    _user = get_valid_user(request)
    if not _user:
        return HttpResponseRedirect('/login')
    try:
        domain=Domain.objects.get(id=domain_id)
    except:
        messages.add_message(request, messages.INFO, ('未找到此域名 !'))
        return HttpResponseRedirect('/itsm/domain-management')
    permit_delete=permit_delete_domain(_user, domain)
    return render(request, 'itsm_domaininfo.html', {'domain':domain, 'permit_delete':permit_delete})


def change_management(request):
    _user = get_valid_user(request)
    if not _user:
        return HttpResponseRedirect('/login')
    return render(request, 'itsm_change.html', {'current_user': _user})


def event_management(request):
    _user = get_valid_user(request)
    if not _user:
        return HttpResponseRedirect('/login')
    return render(request, 'itsm_event.html', {'current_user': _user})



def problem_management(request):
    _user = get_valid_user(request)
    if not _user:
        return HttpResponseRedirect('/login')
    return render(request, 'itsm_problem.html', {'current_user': _user})
