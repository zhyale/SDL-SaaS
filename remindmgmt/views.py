# coding=utf-8
from django.shortcuts import render
from usermgmt.utils import get_valid_user
from usermgmt.models import User
from django.http import HttpResponseRedirect
from django.utils.timezone import localtime
from django.contrib import messages
from models import *
import datetime
import re


# Create your views here.
def show_reminds(request):
    _user = get_valid_user(request)
    if not _user:
        return HttpResponseRedirect('/login')
    deadline_reminds=DeadlineRemind.objects.filter(create_user=_user, is_finished=False)
    period_reminds=PeriodRemind.objects.filter(create_user=_user, is_finished=False)
    onetime_reminds=OneTimeRemind.objects.filter(create_user=_user, is_finished=False)
    pre_30day_time=timezone.now()-datetime.timedelta(days=31)
    finished_reminds=Remind.objects.filter(create_user=_user, is_finished=True, finish_time__gte=pre_30day_time).order_by("-finish_time")
    Remind.objects.filter(create_user=_user, is_finished=True, finish_time__lt=pre_30day_time).delete()
    return render(request, 'remindmgmt_list.html', {'current_user': _user,
                                                 'deadline_reminds':deadline_reminds,
                                                 'period_reminds':period_reminds,
                                                 'onetime_reminds':onetime_reminds,
                                                 'finished_reminds':finished_reminds})

def create_remind(request, remind_method):
    _user = get_valid_user(request)
    if not _user:
        return HttpResponseRedirect('/login')
    cur_time=timezone.now()
    if request.method=="GET":
        remind_method=str.upper(str(remind_method))
        first_time=localtime(cur_time+datetime.timedelta(hours=1, minutes=-cur_time.minute)).strftime("%y-%m-%d %H:%M")
        return render(request, "remindmgmt_create.html",{'current_user': _user, 'first_time':first_time, 'remind_method':remind_method})
    remind_method=request.POST.get("remind_method")
    first_time_or_deadline=datetime.datetime.strptime(request.POST.get("first_time_or_deadline"), "%Y-%m-%d %H:%M")
    first_time_or_deadline=first_time_or_deadline.replace(tzinfo=UTC8())
    title=request.POST.get("title","")
    content=request.POST.get("content","")
    extra_recipient=request.POST.get("extra_recipient",None)
    _remind=None
    if remind_method=="DEADLINE":
        _remind=DeadlineRemind.objects.create(create_user=_user,
                                              title=title, content=content,
                                              extra_recipient=extra_recipient,
                                              remind_method=remind_method,
                                              deadline_time=first_time_or_deadline)
    elif remind_method=="PERD":
        expire_delta=int(request.POST.get("expire_delta"))
        expire_time=first_time_or_deadline+datetime.timedelta(seconds=expire_delta)
        interval=request.POST.get("interval","")
        repeat_method="FIX"
        interval_seconds=0
        if re.match(r"\d+", interval):
            interval_seconds=int(interval)
            if interval_seconds<86400:
                interval_seconds=86400
        elif interval == "MONTHLY":
            interval_seconds=0
            repeat_method="MONTHLY"
        elif interval == "YEARLY":
            interval_seconds=0
            repeat_method="YEARLY"
        _remind=PeriodRemind.objects.create(create_user=_user,
                                            title=title, content=content,
                                            extra_recipient=extra_recipient,
                                            remind_method=remind_method,
                                            first_remind_time=first_time_or_deadline,
                                            repeat_method=repeat_method,
                                            interval_seconds=interval_seconds,
                                            expire_time=expire_time
                                            )
    elif remind_method=="ONETIME":
        _remind=OneTimeRemind.objects.create(create_user=_user,
                                              title=title, content=content,
                                              extra_recipient=extra_recipient,
                                              remind_method=remind_method,
                                              remind_time=first_time_or_deadline)
    if _remind:
        _receivers = request.POST.getlist("receivers", [])
        for receiver_id in _receivers:
            if receiver_id:
                _receiver = User.objects.get(id=receiver_id)
                _remind.receivers.add(_receiver)
        _remind.save()
        messages.add_message(request, messages.INFO, '提醒已创建！')
    return HttpResponseRedirect('/reminds')


def mark_remind_finish(request, remind_id):
    _user = get_valid_user(request)
    if not _user:
        return HttpResponseRedirect('/login')
    try:
        remind=Remind.objects.get(id=remind_id)
        if remind.create_user==_user:
            remind.is_finished=True
            remind.save()
            messages.add_message(request, messages.INFO, '指定的提醒已标记为完成！')
        else:
            messages.add_message(request, messages.INFO, '您无权操作！')
    except:
        messages.add_message(request, messages.INFO, '提醒不存在！')
    return HttpResponseRedirect('/reminds')


def mark_remind_unfinish(request, remind_id):
    _user = get_valid_user(request)
    if not _user:
        return HttpResponseRedirect('/login')
    try:
        remind=Remind.objects.get(id=remind_id)
        if remind.create_user==_user:
            remind.is_finished=False
            remind.save()
            messages.add_message(request, messages.INFO, '指定的提醒已标记为未完成！')
        else:
            messages.add_message(request, messages.INFO, '您无权操作！')
    except:
        messages.add_message(request, messages.INFO, '提醒不存在！')
    return HttpResponseRedirect('/reminds')
