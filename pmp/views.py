# coding=utf-8
from usermgmt.utils import get_valid_user
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import F
from cache import get_guest_index_cache, get_project_flow_by_type, get_project_flow_json_by_id, get_front_pages,get_carousel_pages, clear_cache_by_key, get_cache_value_by_key, get_site_map, get_robots
from django.contrib import messages
import datetime
import re


def show_frontpage(request):
    _user = get_valid_user(request)
    if not _user:
        response = get_guest_index_cache(request)
        return response
    else:
        project_agl_flow = get_project_flow_by_type('AGL')
        # _project_app_flow = get_project_flow_by_type('APP')
        agl_flow_json = get_project_flow_json_by_id(project_agl_flow.id)
        # app_flow_json = get_project_flow_json_by_id(_project_app_flow.id)
        _pages = get_front_pages()
        _carousel_pages=get_carousel_pages()
        _projects = _user.current_handler_projects.all()
        _handler_tasks = _user.current_handler_tasks.filter(
            project__phase=F('done_in_project_phase')) | _user.current_handler_tasks.filter(project__isnull=True)
        # _future_tasks = _user.current_handler_tasks.filter(project__isnull=False).exclude(project__phase=F('done_in_project_phase'))
        return render(request, 'index.html', {'current_user': _user,
                                              'handler_projects': _projects,
                                              'handler_tasks': _handler_tasks,
                                              'agl_flow_json': agl_flow_json,
                                              'pages': _pages,
                                              'carousel_pages': _carousel_pages})



def cache_management(request):
    _user = get_valid_user(request)
    if _user:
        if request.method=="GET":
            return render(request, 'cache.html',{'current_user':_user})
        elif request.method=="POST":
            time_str=datetime.datetime.now().strftime("%m%d%H%M")
            passcode=request.POST.get("passcode","")
            if time_str==str(passcode):
                key=request.POST.get("key","")
                if key:
                    do=request.POST.get("do","")
                    if do=="clear":
                        clear_cache_by_key(key)
                        messages.add_message(request, messages.INFO, ('已清除Cache: %s ！' % key))
                    elif do=="view":
                        cache_value=get_cache_value_by_key(key)
                        if not cache_value:
                            messages.add_message(request, messages.INFO, ('Cache for %s 不存在!' % key))
                        return render(request, 'cache.html',{'current_user':_user, 'cache_value':cache_value})
                else:
                    messages.add_message(request, messages.INFO, ('请输入key！' % key))
            else:
                messages.add_message(request, messages.INFO, ('口令错误!'))
            return render(request, 'cache.html',{'current_user':_user})
    return HttpResponseRedirect('/login')


def show_site_map(request):
    xml = get_site_map()
    return HttpResponse(xml, content_type='application/xml')


def show_robots(request):
    robots=get_robots()
    return HttpResponse(robots, content_type='text/plain')


def show_term(request):
    _user = get_valid_user(request)
    return render(request, 'term.html', {'current_user': _user})


def show_faq(request):
    _user = get_valid_user(request)
    return render(request, 'faq.html', {'current_user': _user})


def debug(request):
    return render(request, 'debug.html', {})


def aboutus(request):
    return render(request, 'aboutus.html', {})
