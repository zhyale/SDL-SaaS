# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from remindmgmt.models import *
from django.core import mail
from django.utils import timezone
from remindmgmt.utils import create_mail_message
import pmp.settings
import datetime


TIME_DELTA_TO_DEADLINE = [datetime.timedelta(days=60),
                          datetime.timedelta(days=45),
                          datetime.timedelta(days=30),
                          datetime.timedelta(days=15),
                          datetime.timedelta(days=7),
                          datetime.timedelta(days=3),
                          datetime.timedelta(days=2),
                          datetime.timedelta(days=1),
                          datetime.timedelta(hours=6),
                          datetime.timedelta(hours=2),
                          datetime.timedelta(minutes=30),
                          datetime.timedelta(minutes=10),
                          datetime.timedelta(seconds=0)]


class Command(BaseCommand):
    # crontab
    # */5 * * * * nobody /path/to/venv/bin/python /path/to/manage.py schedule
    def handle(self, *args, **options):
        cur_time = timezone.now()
        mail_list=[]
        # Deadline Remind
        reminds = DeadlineRemind.objects.filter(is_finished=False)
        for remind in reminds:
            deadline = remind.deadline_time
            if cur_time >= deadline:
                remind.is_finished = True
                remind.save()
                mail_message=create_mail_message(remind, u"【过期提醒】")
                mail_list.append(mail_message)
            else:
                for time_delta in TIME_DELTA_TO_DEADLINE:
                    accurate_remind_time = deadline - time_delta
                    timediff_seconds = abs((cur_time - accurate_remind_time).total_seconds())
                    if timediff_seconds < 300.0:
                        _seconds_delta = time_delta.total_seconds()
                        try:
                            remind_log = RemindLog.objects.get(remind=remind, seconds_delta=_seconds_delta)
                        except:
                            RemindLog.objects.create(remind=remind, seconds_delta=_seconds_delta)
                            mail_message=create_mail_message(remind, u"【提醒】")
                            mail_list.append(mail_message)
                            break
        reminds = PeriodRemind.objects.filter(is_finished=False)
        for remind in reminds:
            if cur_time >= remind.expire_time:
                remind.is_finished = True
                remind.save()
                mail_message=create_mail_message(remind, u"【过期提醒】")
                mail_list.append(mail_message)
            else:
                first_remind_time = remind.first_remind_time
                timediff_seconds = abs((cur_time - first_remind_time).total_seconds())
                seconds_delta=0
                if remind.repeat_method=="FIX":
                    seconds_delta = int(round(timediff_seconds/remind.interval_seconds))*remind.interval_seconds
                elif remind.repeat_method=="MONTHLY":
                    if cur_time.day==first_remind_time.day:
                        seconds_delta = int(round(timediff_seconds/86400))*86400
                elif remind.repeat_method=="YEARLY":
                    if cur_time.month==first_remind_time.month and cur_time.day==first_remind_time.day:
                        seconds_delta = int(round(timediff_seconds/86400))*86400
                if abs(timediff_seconds-seconds_delta)<300.0:
                    try:
                        remind_log = RemindLog.objects.get(remind=remind, seconds_delta=seconds_delta)
                    except:
                        RemindLog.objects.create(remind=remind, seconds_delta=seconds_delta)
                        mail_message=create_mail_message(remind, u"【提醒】")
                        mail_list.append(mail_message)
        reminds = OneTimeRemind.objects.filter(is_finished=False)
        for remind in reminds:
            if cur_time >= remind.remind_time:
                remind.is_finished = True
                remind.save()
                mail_message=create_mail_message(remind, u"【过期提醒】")
                mail_list.append(mail_message)
            else:
                timediff_seconds = abs((cur_time - remind.remind_time).total_seconds())
                if timediff_seconds < 300.0:
                    try:
                        remind_log = RemindLog.objects.get(remind=remind)
                    except:
                        RemindLog.objects.create(remind=remind, seconds_delta=0)
                        mail_message=create_mail_message(remind, u"【提醒】")
                        mail_list.append(mail_message)
        conn=mail.get_connection(fail_silently=(not pmp.settings.DEBUG))
        conn.send_messages(mail_list)
