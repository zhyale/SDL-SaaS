# coding=utf-8
from django.db import models
from usermgmt.models import User
from django.utils import timezone
import datetime


REMIND_CHOICES = (
    ('DEADLINE', '到期提醒'),
    ('PERD', '周期性提醒'),
    ('ONETIME', '仅提醒一次'),
)


# for PeriodRemind
PERIOD_CHOICES = (
    ('FIX', '固定间隔'),
    ('MONTHLY', '按月提醒'),
    ('YEARLY', '按年提醒'),
)


class Remind(models.Model):
    create_time=models.DateTimeField(auto_now_add=True)
    create_user=models.ForeignKey(User, related_name='create_user_reminds')
    title=models.CharField(max_length=256)
    content=models.CharField(max_length=1024, null=True, blank=True)
    receivers=models.ManyToManyField(User, related_name='receiver_reminds')
    extra_recipient=models.EmailField(null=True, blank=True)
    remind_method=models.CharField(max_length=16, choices=REMIND_CHOICES, default='DEADLINE')
    is_finished=models.BooleanField(default=False)
    finish_time=models.DateTimeField(auto_now=True)
    # op_code=models.CharField(max_length=16)

    def __unicode__(self):
        return self.title


class DeadlineRemind(Remind):
    deadline_time=models.DateTimeField(null=True, blank=True)


class PeriodRemind(Remind):
    first_remind_time=models.DateTimeField()
    repeat_method=models.CharField(max_length=16, choices=PERIOD_CHOICES, default='FIX')
    interval_seconds=models.BigIntegerField()
    expire_time=models.DateTimeField(default=timezone.datetime.max)

    def get_interval_description(self):
        if self.repeat_method=="MONTHLY":
            return u"每月"
        elif self.repeat_method=="YEARLY":
            return u"每年"
        else:
            time_str="每"
            int_seconds=self.interval_seconds
            if int_seconds>=86400:
                time_str+=str(int_seconds/86400)+"天"
                int_seconds=int_seconds % 86400
            if int_seconds>=3600:
                time_str+=str(int_seconds/3600)+"小时"
                int_seconds=int_seconds % 3600
            if int_seconds>=60:
                time_str+=str(int_seconds/60)+"分钟"
        return time_str

class OneTimeRemind(Remind):
    remind_time=models.DateTimeField()


class RemindLog(models.Model):
    log_time=models.DateTimeField(auto_now_add=True)
    remind=models.ForeignKey(Remind, related_name='remind_logs')
    seconds_delta=models.BigIntegerField() # seconds to deadline, or from first remind.


class UTC8(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(seconds=28800)

    def dst(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return "UTC8"
