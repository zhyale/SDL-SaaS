#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from usermgmt.models import *
from usermgmt.utils import get_valid_user, auth_by_rsa, get_decrypted_pwd, change_to_new_email, is_free_email, sso_generate_ticket, sso_get_ticket_data
from msgmgmt.utils import send_msg, send_circle_msg
import os,time
import base64
import hashlib
import random
import pmp.settings
from django.core.mail import EmailMessage,send_mail
from PIL import Image
from django.db.models import Q
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def Register(request):
    _username=request.POST.get("username","")
    if _username:
        _email=request.POST.get("email","")
        if is_free_email(_email):
            messages.add_message(request, messages.INFO, '请使用有效的办公邮件地址（不支持免费邮箱）注册！')
            return render(request,'userreg.html',{})
        _cipher_pwd=request.POST.get("password","")
        try:
            _user=User.objects.get(email=_email)
        except:
            _salt=base64.b64encode(os.urandom(6))
            _password0=get_decrypted_pwd(_cipher_pwd)
            _password2=hashlib.sha512(_password0+_salt).hexdigest()
            _company_domain=_email[_email.index('@')+1:]
            _user=None
            try:
                _company=Company.objects.get(top_domain_name=_company_domain)
            except:
                # The first user for the designated company
                _abbr=_company_domain[0:_company_domain.index('.')][0:3].upper()
                _company=Company.objects.create(top_domain_name=_company_domain, abbr=_abbr)
                _user=User.objects.create(username=_username, salt=_salt, hashpwd=_password2,email=_email,company=_company)
            if not _user:
                # not the first user
                _user=User.objects.create(username=_username, salt=_salt, hashpwd=_password2,email=_email,company=_company)
            _fail_silently=(not pmp.settings.DEBUG)
            send_mail('您在SDL SaaS中注册成功!','您好！\r\n\r\n您在SDL SaaS中已注册成功!\r\n平台地址：'+pmp.settings.SAAS_PORTAL+ '\r\n\r\nBest regards,\r\nJanusec SDL Team',pmp.settings.EMAIL_FROM,[_user.email], fail_silently=_fail_silently)
            messages.add_message(request, messages.INFO, '注册成功!')
            return HttpResponseRedirect('/login')
        messages.add_message(request, messages.INFO, '用户已存在!')
        return render(request,'userreg.html',{})
    return render(request, 'userreg.html', {})

def Login(request):
    if request.method=="GET":
        return render(request, 'login.html', {})
    _email=request.POST.get("email","")
    if(_email==""):
        messages.add_message(request, messages.INFO, '请输入有效的邮件地址!')
        return render(request, 'login.html', {})
    try:
        _user=User.objects.get(email=_email)
    except:
        messages.add_message(request, messages.INFO, '错误的电子邮箱或口令!')
        return render(request, 'login.html', {})
    _user_agent=request.META.get('HTTP_USER_AGENT')
    if not _user_agent:
        messages.add_message(request, messages.INFO, '不支持的浏览器类型!请使用Chrome、IE9+等现代浏览器。')
        return render(request, 'login.html', {})
    _rsa_pwd=request.POST.get("password","")
    if(auth_by_rsa(_user, _rsa_pwd)):
        request.session.set_expiry(86400*30)
        request.session['uid'] = _user.id
        request.session['UA'] = hashlib.md5(_user_agent).hexdigest()
        if _user.need_modify_pwd:
            messages.add_message(request, messages.INFO, '当前口令为系统随机生成，请修改为您自己的口令！')
            return render(request, 'useredit.html',{'current_user':_user})
        response=HttpResponseRedirect('/')
        response.set_cookie('email', _email, max_age=86400*3650)
        return response
    messages.add_message(request, messages.INFO, '错误的电子邮箱或口令!')
    return render(request, 'login.html', {})


def sso_login(request):
    _user=get_valid_user(request)
    redirect_url=request.GET.get("redirect", None)
    if _user:
        if redirect_url:
            appid=request.GET.get("appid","")
            ticket=sso_generate_ticket(appid, _user)
            redirect_url += "?ticket="+ticket
            return HttpResponseRedirect(redirect_url)
        else:
            return HttpResponseRedirect('/')
    else:
        if request.method == "POST":
            _email=request.POST.get("email","")
            if(_email==""):
                messages.add_message(request, messages.INFO, '请输入有效的邮件地址!')
                return render(request, 'login.html', {})
            try:
                _user=User.objects.get(email=_email)
            except:
                messages.add_message(request, messages.INFO, '错误的电子邮箱或口令!')
                return render(request, 'login.html', {})
            _user_agent=request.META.get('HTTP_USER_AGENT')
            if not _user_agent:
                messages.add_message(request, messages.INFO, '不支持的浏览器类型!请使用Chrome、IE9+等现代浏览器。')
                return render(request, 'login.html', {})
            _rsa_pwd=request.POST.get("password","")
            if(auth_by_rsa(_user, _rsa_pwd)):
                request.session.set_expiry(86400*30)
                request.session['uid'] = _user.id
                request.session['UA'] = hashlib.md5(_user_agent).hexdigest()
                if _user.need_modify_pwd:
                    messages.add_message(request, messages.INFO, '当前口令为系统随机生成，请修改为您自己的口令！')
                    return render(request, 'useredit.html',{'current_user':_user})
                if not redirect_url:
                    redirect_url='/'
                else:
                    appid=request.GET.get("appid","")
                    ticket=sso_generate_ticket(appid, _user)
                    redirect_url += "?ticket="+ticket
                response=HttpResponseRedirect(redirect_url)
                response.set_cookie('email', _email, max_age=86400*3650)
                return response
            messages.add_message(request, messages.INFO, '错误的电子邮箱或口令!')
            return render(request, 'login.html', {})
        else:
            return render(request,'login.html',{})


def get_user_by_ticket(request):
    ticket=request.GET.get("ticket",None)
    if ticket:
        ticket_data=sso_get_ticket_data(ticket)
        if ticket_data:
            auth_user=ticket_data["user"]
            response={'uid':auth_user.id, 'username':auth_user.username, 'avatar': pmp.settings.SAAS_PORTAL + auth_user.display_avatar_link()}
            return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json")
    return HttpResponse("{}", content_type="application/json")


def Logout(request):
    if request.session.get("uid",""):
        del request.session['uid']
        del request.session['UA']
    messages.add_message(request, messages.INFO, '您已安全退出!')
    # return render(request, 'login.html', {})
    return HttpResponseRedirect('/login')


def UserInfo(request, query_uid):
    _user=get_valid_user(request)
    if _user:
        _quid=int(query_uid)
        try:
            _quser=User.objects.get(id=_quid)
        except:
            _quser=None
        if _quser:
            if _user.company==_quser.company or _quser.email=="jane@janusec.com":
                return render(request, 'userinfo.html', {'current_user':_user, 'query_user':_quser})
        messages.add_message(request, messages.INFO, '您没有查看该用户资料的权限！')
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/login')

def ChangeDefaultTeam(request):
    _user=get_valid_user(request)
    if _user:
        _tid=request.POST.get("tid","")
        _team=Team.objects.get(id=_tid)
        _user.default_team=_team
        _user.save()
        referer=request.META['HTTP_REFERER']
        return HttpResponseRedirect(referer)

def UserLostPassword(request):
    if request.method=="GET":
        return render(request,'userlostpwd.html',{})
    _email=request.POST.get("email")
    try:
        _user=User.objects.get(email=_email)
    except:
        messages.add_message(request, messages.INFO, '您输入的邮箱 '+_email+' 不存在，请检查后重新输入！')
        return render(request,'userlostpwd.html',{})
    _rand_pwd=base64.b64encode(os.urandom(6))
    _user.hashpwd=hashlib.sha512(_rand_pwd+_user.salt).hexdigest()
    _user.need_modify_pwd=True
    _user.save()
    _fail_silently=(not pmp.settings.DEBUG)
    send_mail('您在SDL SaaS中的密码!','您好！\r\n\r\n您在SDL SaaS中的密码已重置为：'+ _rand_pwd+' ，请登录后修改!\r\nSDL系统地址：'+pmp.settings.SAAS_PORTAL+ '\r\n\r\nSDL Team',pmp.settings.EMAIL_FROM,[_user.email], fail_silently=_fail_silently)
    messages.add_message(request, messages.INFO, '您的密码已重置并发送到您注册的邮箱，请查收!')
    return HttpResponseRedirect('/login')


def make_thumb(path, thumb_path, size):
    img = Image.open(path)
    width, height = img.size
    if width > height:
        delta = (width - height) / 2
        box = (delta, 0, width - delta, height)
        region = img.crop(box)
    elif height > width:
        delta = (height - width) / 2
        box = (0, delta, width, height - delta)
        region = img.crop(box)
    else:
        region = img
    thumb = region.resize((size, size), Image.ANTIALIAS)
    base, ext = os.path.splitext(os.path.basename(path))
    _short_filename=base+'_thumb.jpg'
    filename = os.path.join(thumb_path, _short_filename)
    thumb.save(filename, quality=100)
    return _short_filename

def UserEdit(request):
    _user=get_valid_user(request)
    if _user:
        if request.method=="GET":
            return render(request, 'useredit.html', {'current_user':_user})
        _username=request.POST.get("username","")
        if _username:
            _user.username=_username
        _nickname=request.POST.get("nickname","")
        if _nickname:
            _user.nickname=_nickname
        _avatar=request.FILES.get("avatar","")
        if _avatar:
            _ext=_avatar.name.split('.').pop()
            _short_filename=time.strftime('%Y%m%d%H%M%S')+str(random.randint(100000,999999))+"."+_ext
            _origin_filename='./media/upload/avatars/original/'+ _short_filename
            dest_file=open(_origin_filename, 'wb+')
            for chunk in _avatar.chunks():
                dest_file.write(chunk)
            dest_file.close()
            _thumb_short_filename = make_thumb(_origin_filename, './media/upload/avatars/thumb/', 50)
            _user.avatar_link='/media/upload/avatars/thumb/'+_thumb_short_filename
        _oldpwd_cipher=request.POST.get("oldpwd","")
        if _oldpwd_cipher:
            _oldpwd=get_decrypted_pwd(_oldpwd_cipher)
            if(hashlib.sha512(_oldpwd+_user.salt).hexdigest()==_user.hashpwd):
                _newpwd_cipher=request.POST.get("newpwd","")
                if _newpwd_cipher:
                    _newpwd=get_decrypted_pwd(_newpwd_cipher)
                    _new_salt=base64.b64encode(os.urandom(6))
                    _user.salt=_new_salt
                    _user.hashpwd=hashlib.sha512(_newpwd+_new_salt).hexdigest()
                    messages.add_message(request, messages.INFO, '密码已修改，请记住新密码!')
                    _user.need_modify_pwd=False
                else:
                    messages.add_message(request, messages.INFO, '新密码不能为空！')
                    return render(request, 'useredit.html', {'current_user':_user})
            else:
                messages.add_message(request, messages.INFO, '旧密码输入错误，密码未修改!')
        _user.location=request.POST.get("location","")
        _user.department=request.POST.get("department","")
        _user.mobile=request.POST.get("mobile","")
        _user.introduction=request.POST.get("introduction","")
        _user.save()
        messages.add_message(request, messages.INFO, '用户资料已修改!')
        return render(request, 'userinfo.html', {'current_user':_user, 'query_user':_user})
    return HttpResponseRedirect('/login')

def SearchUsers(request):
    _uid=request.session.get("uid","")
    _keyword=request.GET.get("s","")
    if _uid and len(_keyword)>=3:
        _current_user=User.objects.get(id=_uid)
        _users=User.objects.filter(company=_current_user.company).filter(Q(email__startswith=_keyword)|Q(username__icontains=_keyword))
        #_users=_current_user.default_team.members.filter(Q(email__startswith=_keyword)|Q(username__icontains=_keyword))
        _userlist=[]
        for _user in _users:
            _userlist.append({'uid':_user.id, 'username':_user.username,'email':_user.email,'avatar':_user.display_avatar_link()})
            if len(_userlist)>=10:
                break
        _result_json=json.JSONEncoder().encode(_userlist)
        # if pmp.settings.DEBUG:
        #     time.sleep(1)
        return HttpResponse(_result_json,  content_type="application/json")
    return HttpResponse('[]',  content_type="application/json")

def SearchUser(request):
    _uid=request.session.get("uid","")
    _keyword=request.GET.get("s","")
    if _uid and len(_keyword)>=3:
        _users=User.objects.filter(username__startswith=_keyword)
        _users_str=''
        if len(_users)>0:
            for _user in _users:
                if len(_users_str)>0:
                    _users_str=_users_str+', '
                _users_str=_users_str +_user.username
            return HttpResponse(_users_str, content_type="text/plain")
    return HttpResponse('No user found!',  content_type="text/plain")


# Team

def TeamList(request):
    _user=get_valid_user(request)
    if _user:
        _admin_teams=_user.admin_teams.all()
        _member_teams=_user.member_teams.all()
        _company_teams=_user.company.company_teams.all()
        return render(request,'teamlist.html',{'current_user':_user,'admin_teams':_admin_teams,'member_teams':_member_teams,'company_teams':_company_teams})
    return HttpResponseRedirect('/login')

def TeamInfo(request,tid):
    _user=get_valid_user(request)
    if _user:
        _tid=int(tid)
        try:
            _team=Team.objects.get(id=_tid)
            if _team.company <> _user.company:
                messages.add_message(request, messages.INFO, '您没有权限查看该团队信息！')
                return  render(request, 'index.html', {'current_user':_user})
        except:
            messages.add_message(request, messages.INFO, '您没有权限查看该团队信息！')
            return render(request, 'index.html', {'current_user':_user})
        team_can_be_deleted=False
        if _user in _team.admins.all():
            _team.members.add(_user)
            _team.save()
            if _team.members.count()<2 and _team.team_projects.count()==0:
                team_can_be_deleted=True
        return render(request,'teaminfo.html',{'current_user':_user,'team':_team, 'team_can_be_deleted':team_can_be_deleted})
    return HttpResponseRedirect('/login')

def TeamCreate(request):
    _user=get_valid_user(request)
    if _user and request.method=="POST":
        _name=request.POST.get("name","")
        if _name:
            _abbr=request.POST.get("abbr","")
            _team=Team.objects.create(name=_name, company=_user.company, abbr=_abbr)
            _team.admins.add(_user)
            _team.members.add(_user)
            _team.save()
            _user.default_team=_team;
            _user.save()
        return HttpResponseRedirect('/team')
    return HttpResponseRedirect('/login')

def TeamChange(request):
    _user=get_valid_user(request)
    if _user and request.method=="POST":
        _do=request.POST.get("do","")
        _tid=request.POST.get("tid")
        _team=Team.objects.get(id=_tid)
        if _user not in _team.members.all():
            messages.add_message(request, messages.INFO, '您没有权限修改团队资料！')
            return render(request, 'index.html', {'current_user':_user})
        if _do=="addmember":
            _username=request.POST.get("username")
            if not _username:
                messages.add_message(request, messages.INFO, '请输入真实有效的用户名（电子邮件地址中@前面的部分）！')
                return render(request,'teaminfo.html',{'current_user':_user,'team':_team})
            _email=_username+"@"+_user.company.top_domain_name
            try:
                _new_member=User.objects.get(email=_email)
            except:
                _new_member=User.objects.create(username=_username,email=_email,company=_user.company, need_modify_pwd=True,default_team=_team)
                _fail_silently=(not pmp.settings.DEBUG)
                mail_body='''您好！
                %s 将您添加到团队【%s】 ，初始口令为: Flzx3000c
                请及时登录并修改口令： %s

                SDL SaaS''' % (_user.username, _team.name, pmp.settings.SAAS_PORTAL)
                send_mail('您已加入【%s】团队!' % _team.name, mail_body, pmp.settings.EMAIL_FROM,[_new_member.email], fail_silently=_fail_silently)
            if _new_member not in _team.members.all():
                _team.members.add(_new_member)
                send_msg(_user, _new_member, '我已将您加入【%s】团队' % _team.name)
                send_circle_msg(_user, '热烈欢迎 %s 加入【%s】团队' % (_new_member.username, _team.name))
        elif _do=="addadmin":
            _uid=int(request.POST.get("uid"))
            _new_admin=User.objects.get(id=_uid)
            _team.admins.add(_new_admin)
        elif _do=="removemember":
            _uid=int(request.POST.get("uid"))
            _member=User.objects.get(id=_uid)
            _team.members.remove(_member)
        elif _do=="removeadmin":
            _uid=int(request.POST.get("uid"))
            _admin=User.objects.get(id=_uid)
            if _team.admins.count()>1:
                _team.admins.remove(_admin)
            else:
                messages.add_message(request, messages.INFO, '请先添加一名管理员然后才能删除！')
                return render(request,'teaminfo.html',{'current_user':_user,'team':_team})
        elif _do=="del":
            if _user in _team.admins.all() and _team.members.count()<2 and _team.team_projects.count()==0:
                for member in _team.default_team_users.all():
                    member.default_team=None
                    member.save()
                _team.delete()
                messages.add_message(request, messages.INFO, '已删除指定的团队！')
                return HttpResponseRedirect("/team")
        _team.save()
        return HttpResponseRedirect("/team/"+str(_team.id))
    return HttpResponseRedirect('/login')


def change_corporation(request):
    _user=get_valid_user(request)
    if _user:
        if request.method=="GET":
            return render(request, 'userchangecorp.html',{'current_user':_user})
        elif request.method=="POST":
            new_email=request.POST.get("new_email","")
            if not new_email:
                messages.add_message(request, messages.INFO, '请输入新的Email地址！')
                return render(request, 'userchangecorp.html',{'current_user':_user})
            check_code=request.POST.get("check_code","")
            if not check_code:
                check_code=base64.b64encode(os.urandom(6))
                _user.check_code=check_code
                _user.save()
                _fail_silently=(not pmp.settings.DEBUG)
                mail_body='''您好！

                您的Email地址变更请求已收到，请在当前打开的网页中输入如下验证码（可以复制）：
                %s

                SDL SaaS''' % (check_code)
                send_mail('Email校验-SDL SaaS', mail_body, pmp.settings.EMAIL_FROM,[new_email], fail_silently=_fail_silently)
                return render(request, 'userchangecorp.html',{'current_user':_user, 'new_email':new_email})
            if _user.check_code==check_code:
                change_to_new_email(_user, new_email)
                messages.add_message(request, messages.INFO, '修改成功，新Email地址已生效！')
                return render(request, 'userinfo.html', {'current_user':_user, 'query_user':_user})
    return HttpResponseRedirect('/login')