#coding=utf-8
from models import *
from usermgmt.utils import get_valid_user, get_user_display_name
from django.http import HttpResponseRedirect
from django.shortcuts import render
from utils import collect_user_suggest, to_html_msg, send_msg
import pmp.settings


def MessageList(request):
    _user=get_valid_user(request)
    if _user:
        _received_msgs=Message.objects.filter(receiver=_user, source=None, receiver_delete=False).order_by('-last_reply_time')
        _sent_msgs=Message.objects.filter(sender=_user, source=None, sender_delete=False).order_by('-last_reply_time')
        if request.method=='GET':
            unviewed_msgs=Message.objects.filter(receiver=_user, receiver_delete=False)
            for msg in unviewed_msgs:
                if not msg.viewed:
                    msg.viewed=True
                    msg.save()
            return render(request, 'msglist.html', {'current_user':_user,
                                                    'received_msgs':_received_msgs,
                                                    'sent_msgs':_sent_msgs})
        else:
            _receiver_id=request.POST.get("receiver_id","")
            _receiver=User.objects.get(id=_receiver_id)
            _msg=request.POST.get("msg")
            _source=None
            _source_id=request.POST.get("source_id","")
            if _source_id:
                _source=Message.objects.get(id=_source_id)
                _source.sender_delete=False
                _source.receiver_delete=False
                _source.save()
            Message.objects.create(sender=_user,
                                   receiver=_receiver,
                                   body=to_html_msg(_msg),
                                   source=_source)
            return render(request, 'msglist.html', {'current_user':_user,
                                                    'received_msgs':_received_msgs,
                                                    'sent_msgs':_sent_msgs})
    return HttpResponseRedirect('/login')

def MessageDelete(request):
    _user=get_valid_user(request)
    if _user:
        _mid=request.POST.get("mid","")
        if _mid:
            _message=Message.objects.get(id=_mid)
            if _message.sender==_user:
                _message.sender_delete=True
            if _message.receiver==_user:
                _message.receiver_delete=True
            if _message.sender_delete and _message.receiver_delete:
                _message.delete()
            else:
                _message.save()
        return HttpResponseRedirect('msglist')
    return HttpResponseRedirect('/login')

def Suggest(request):
    _user=get_valid_user(request)
    if _user:
        if request.method=='GET':
            _receiver=User.objects.get(email='jane@janusec.com')
            return render(request, 'suggest.html', {'current_user':_user, 'receiver':_receiver})
        _msg=request.POST.get("msg","")
        collect_user_suggest(_user, _msg)
        return HttpResponseRedirect('/msglist')
    return HttpResponseRedirect('/login')

def Circle(request):
    _user=get_valid_user(request)
    if _user:
        if request.method=='GET':
            _team_msgs=CircleMessage.objects.filter(source=None, sender__member_teams__in=_user.member_teams.all()).distinct().order_by('-last_reply_time')
            _company_msgs=CircleMessage.objects.filter(source=None, sender__company=_user.company).exclude(sender__member_teams__in=_user.member_teams.all()).distinct().order_by('-last_reply_time')
            return render(request, 'circle.html', {'current_user':_user,
                                                   'team_msgs':_team_msgs,
                                                   'company_msgs':_company_msgs})
        else:
            _source=None
            _source_id=request.POST.get("source_id","")
            _msg=request.POST.get("msg","")
            if _source_id: # reply or appreciate
                _source=CircleMessage.objects.get(id=_source_id)
                _anonymous=_source.anonymous
                _notice=get_user_display_name(_user, _anonymous)
                if _msg: # reply
                    CircleMessage.objects.create(sender=_user,
                                       body=to_html_msg(_msg),
                                       anonymous=_anonymous,
                                       source=_source)

                    _notice += ' 回复了您的工作圈文章 '+ pmp.settings.SAAS_PORTAL+'/circle'
                else:  # appreciate
                    _source.praised_by.add(_user)
                    _notice += ' 赞了您的工作圈文章 '+ pmp.settings.SAAS_PORTAL+'/circle'
                _source.save()

                send_msg(None, _source.sender, _notice)
            else:   # new circle message
                _anonymous=int(request.POST.get("anonymous", 0))
                if _anonymous>0:
                    _anonymous=True
                else:
                    _anonymous=False
                if _msg:
                    CircleMessage.objects.create(sender=_user,
                                       body=to_html_msg(_msg),
                                       anonymous=_anonymous,
                                       source=_source)
            return HttpResponseRedirect('/circle')
    return HttpResponseRedirect('/login')

def CircleDelete(request):
    _user=get_valid_user(request)
    if _user:
        _mid=request.POST.get("mid","")
        if _mid:
            _message=CircleMessage.objects.get(id=_mid)
            _message.delete()
        return HttpResponseRedirect('/circle')
    return HttpResponseRedirect('/login')