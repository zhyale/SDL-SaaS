#coding=utf-8
from usermgmt.models import User
from models import Message, CircleMessage
import re

def to_html_msg(_msg):
    _msg=_msg.replace("<", "&lt;").replace(">", "&gt;").replace("\r\n","<br/>")
    urllist=re.findall(r'https?://[/\w\d\.\-:?=&]+', _msg)
    for url in urllist:
        _msg=_msg.replace(url, ('<a href="%s" target="_blank">%s</a>' % (url, url)))
    return _msg

def send_msg(_sender, _receiver, _msg):
    _body=to_html_msg(_msg)
    Message.objects.create(sender=_sender,
                                   receiver=_receiver,
                                   body=_body,
                                   sender_delete=False if _sender else True,
                                   source=None)

def send_circle_msg(_sender, _msg):
    _body=to_html_msg(_msg)
    CircleMessage.objects.create(sender=_sender,
                                   body=_body,
                                   anonymous=False,
                                   source=None)

def collect_user_suggest(_sender, _msg):
    _body=to_html_msg(_msg)
    Message.objects.create(sender=_sender,
                                   receiver=User.objects.get(email='jane@janusec.com'),
                                   body=_body)