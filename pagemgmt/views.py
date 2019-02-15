# coding=utf-8
from models import *
from django.http import HttpResponseRedirect
from django.shortcuts import render
from usermgmt.utils import get_valid_user
from utils import create_comment
from pmp.cache import get_page_by_pseudo_name


def show_page(request, pseudo_link):
    _user = get_valid_user(request)
    _page = get_page_by_pseudo_name(pseudo_link)
    if request.method == "GET":
        return render(request, 'showpage.html', {'current_user': _user, 'page': _page})
    elif _user:
        # comment
        comment_page_id = request.POST.get("pid")
        comment_page = Page.objects.get(id=comment_page_id)
        if _page == comment_page:
            content = request.POST.get("content", "")[0:100]
            create_comment(_page, _user, content)
    return HttpResponseRedirect('/content/' + pseudo_link)
