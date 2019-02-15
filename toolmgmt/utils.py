# coding=utf-8
from django.core.cache import cache
from models import IpSegment


def get_ip_int(ip):
    ip_list=ip.split('.')
    try:
        ip_int=int(ip_list[0])*pow(256,3) + int(ip_list[1])*pow(256,2) + int(ip_list[2])*256 + int(ip_list[3])
    except:
        ip_int=0
    return ip_int


def get_ip_address(ip):
    addr=cache.get(ip)
    if not addr:
        ip_int=get_ip_int(ip)
        try:
            ip_seg=IpSegment.objects.get(start_int__lte=ip_int, end_int__gte=ip_int)
            addr=ip_seg.address
        except:
            addr='UNKNOWN'
        cache.set(ip, addr, 300)
    if type(addr) is unicode:
        return addr
    return unicode(addr, "utf-8")
