from django.shortcuts import render
from toolmgmt.models import IpSegment
from toolmgmt.utils import get_ip_int, get_ip_address
from usermgmt.utils import get_valid_user
from django.http import HttpResponse,HttpResponseRedirect
import re


# Create your views here.
def init_ip_segment(request):
    ip_count=IpSegment.objects.count()
    if ip_count==0:
        ip_file = open(r'ip.txt', 'r')
        regex=re.compile(r'\s+CZ88\.NET')
        ip_seg_in_batch=[]
        count=0
        for line in ip_file:
            count+=1
            if line:
                line=line.replace("\r\n","")
                line=re.sub(regex,'',line)
                line_list=re.split(ur'[\x20]+',line)
                len_list=len(line_list)
                if len_list>=2:
                    _ip_start=line_list[0]
                    _ip_end=line_list[1]
                    _start_int=get_ip_int(_ip_start)
                    _end_int=get_ip_int(_ip_end)
                    if len_list==2:
                        _address="UNKNOWN"
                    else:
                        _address=unicode('_'.join(line_list[2:]), "utf-8")
                    ip_seg=IpSegment(ip_start=_ip_start, ip_end=_ip_end,
                                     start_int=_start_int, end_int=_end_int,
                                     address=_address)
                    ip_seg_in_batch.append(ip_seg)
                else:
                    print("list<3"+line)
            if len(ip_seg_in_batch)>=5000:
                IpSegment.objects.bulk_create(ip_seg_in_batch)
                ip_seg_in_batch=[]
                print("count="+str(count))
        ip_file.close()
        if len(ip_seg_in_batch)>0:
            IpSegment.objects.bulk_create(ip_seg_in_batch)
        return HttpResponse("OK")


def ip_address_portal(request):
    ip=""
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    addr=get_ip_address(ip)
    _user=get_valid_user(request)
    return render(request, 'toolmgmt_ip.html', {'current_user':_user, 'ip':ip, 'address':addr})


def ip_address(request, ip):
    addr=get_ip_address(ip)
    _user=get_valid_user(request)
    return render(request, 'toolmgmt_ip.html', {'current_user':_user, 'ip':ip, 'address':addr})


def show_tools(request):
    _user=get_valid_user(request)
    return render(request, 'toolmgmt_tools.html', {'current_user':_user})
