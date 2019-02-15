# coding=utf-8
from models import User, Company, Team
from msgmgmt.models import Message
from pmp.cache import get_priv_key, update_today_statistics
from django.core.cache import cache
import rsa
import hashlib
import base64
import os
import re


def get_decrypted_pwd(cipher_pwd):
    priv_key = get_priv_key()
    cipher_pwd = ''.join([chr(int(x, 16)) for x in re.findall(r'\w\w', cipher_pwd)])
    password0 = rsa.decrypt(cipher_pwd, priv_key)
    return password0


def auth_by_rsa(_user, cipher_pwd):
    password0 = get_decrypted_pwd(cipher_pwd)
    if hashlib.sha512(password0 + _user.salt).hexdigest() == _user.hashpwd:
        _teams = _user.member_teams.all()
        if _teams and not _user.default_team:
            _user.default_team = _teams[0]
        _user.save()
        return True
    return False


def get_valid_user(request):
    current_user=None
    try:
        _uid = request.session.get("uid", "")
        if _uid:
            _legal_ua = request.session.get("UA", "")
            if _legal_ua:
                _current_ua = request.META.get("HTTP_USER_AGENT", "")
                if _current_ua:
                    _current_ua = hashlib.md5(_current_ua).hexdigest()
                    if _current_ua == _legal_ua:
                        _user = User.objects.get(id=_uid)
                        request.session['unviewed_msgs_count'] = Message.objects.filter(receiver=_user,
                                                                                        viewed=False).count()
                        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                            _user.last_login_ip = request.META['HTTP_X_FORWARDED_FOR']
                        else:
                            _user.last_login_ip = request.META['REMOTE_ADDR']
                        _user.save()
                        current_user = _user
        update_today_statistics(current_user)
        return current_user
    except:
        return None


def get_user_display_name(user, anonymous):
    if anonymous:
        return user.nickname or '匿名用户'
    else:
        return user.username


def is_free_email(email):
    company_domain=email[email.index('@')+1:]
    block_email_domains=["qq.","163.","126.","sina.","hotmail.", "gmail.","yahoo.", "sohu.","outlook.","foxmail."]
    for block_domain in block_email_domains:
        try:
            if company_domain.index(block_domain)==0:
                return True
        except:
            pass
    return False


def change_to_new_email(current_user, new_email):
    prev_teams=current_user.member_teams.all()
    for team in prev_teams:
        team.members.remove(current_user)
        team.admins.remove(current_user)
    current_user.email=new_email
    current_user.email_checked=True
    company_domain=new_email[new_email.index('@')+1:]
    new_company=None
    try:
        new_company=Company.objects.get(top_domain_name=company_domain)
    except:
        _abbr=company_domain[0:company_domain.index('.')][0:3].upper()
        new_company=Company.objects.create(top_domain_name=company_domain, abbr=_abbr)
    current_user.company=new_company
    current_user.default_team=None
    current_user.save()
    return


def init_demo_users():
    try:
        _company = Company.objects.get(top_domain_name='janusec.com')
    except:
        _company = Company.objects.create(top_domain_name='janusec.com', abbr='JAN')
        _team = Team.objects.create(name='华山剑谱管理产品', company=_company, abbr='JAN-ADM')
        User.objects.bulk_create([
            User(username='linghuchong', company=_company, email='linghuchong@janusec.com',
                 avatar_link='/media/upload/avatars/thumb/linghuchong.jpg'),
            User(username='yuelingshan', company=_company, email='yuelingshan@janusec.com',
                 avatar_link='/media/upload/avatars/thumb/yuelingshan.jpg'),
            User(username='yilin', company=_company, email='yilin@janusec.com',
                 avatar_link='/media/upload/avatars/thumb/yilin.jpg'),
            User(username='renyingying', company=_company, email='renyingying@janusec.com',
                 avatar_link='/media/upload/avatars/thumb/renyingying.jpg'),
            User(username='ningzhongze', company=_company, email='ningzhongze@janusec.com',
                 avatar_link='/media/upload/avatars/thumb/ningzhongze.jpg'),
            User(username='fengqingyang', company=_company, email='fengqingyang@janusec.com',
                 avatar_link='/media/upload/avatars/thumb/fengqingyang.jpg'),
            User(username='dongfangbubai', company=_company, email='dongfangbubai@janusec.com',
                 avatar_link='/media/upload/avatars/thumb/dongfangbubai.jpg'),
            User(username='Jane', company=_company, email='jane@janusec.com',
                 avatar_link='/media/upload/avatars/thumb/jane.jpg', location='海外', introduction='预防胜于补救~'),
        ])
        _team.admins.add(User.objects.get(email='linghuchong@janusec.com'))
        _members = User.objects.filter(company=_company)
        for member in _members:
            _team.members.add(member)
        _team.save()


# SSO
def sso_generate_ticket(appid, _user):
    ticket=hashlib.md5(base64.b64encode(os.urandom(8))).hexdigest()
    ticket_data={'appid':appid, 'user':_user}
    cache.set(ticket, ticket_data, 120)
    return ticket


def sso_get_ticket_data(ticket):
    return cache.get(ticket)
