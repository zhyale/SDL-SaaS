# coding=utf-8
from django.utils import timezone
from django.core import mail
import pmp.settings


def create_mail_message(remind, extra_title):
    recipients = []
    for recipient in remind.receivers.all():
        recipients.append(recipient.email)
    if remind.extra_recipient:
        recipients.append(remind.extra_recipient)
    _subject = extra_title + remind.title
    _message = u"【提醒内容】: %s" % remind.content
    _message += u"\r\n【提醒方式】: %s" % remind.get_remind_method_display()
    if remind.remind_method=="DEADLINE":
        _message+="\r\n【Deadline】: %s" % timezone.localtime(remind.deadline_time).strftime("%Y-%m-%d %H:%M")
    elif remind.remind_method=="PERD":
        _message+="\r\n【首次提醒】: %s" % timezone.localtime(remind.first_remind_time).strftime("%Y-%m-%d %H:%M")
        _message+="\r\n【提醒频度】: %s" % remind.get_interval_description()
        _message+="\r\n【过期时间】: %s" % timezone.localtime(remind.expire_time).strftime("%Y-%m-%d %H:%M")
    elif remind.remind_method=="ONETIME":
        _message+="\r\n【提醒时间】: %s" % timezone.localtime(remind.remind_time).strftime("%Y-%m-%d %H:%M")
    _message+="\r\n【创建人员】: %s" % remind.create_user.email
    _message+="\r\n\r\n来自SDL SaaS在线邮件提醒\r\nhttp://saas.janusec.com"
    mail_message=mail.EmailMessage(subject=_subject, body=_message,
                                   from_email=pmp.settings.EMAIL_FROM, to=recipients,
                                   cc=[remind.create_user.email], reply_to=[remind.create_user.email])
    return mail_message
