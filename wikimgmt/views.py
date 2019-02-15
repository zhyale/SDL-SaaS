# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from usermgmt.utils import get_valid_user
from models import *
import json


def show_wiki_by_abbr(request, _abbr):
    wiki_dict = {}
    try:
        wiki = Wiki.objects.get(abbr=_abbr, company__isnull=True)
        print(wiki)
        wiki_dict["expression"] = wiki.expression
        wiki_dict["description"] = wiki.description
    except:
        wiki_dict["expression"] = 'Not Found'
        wiki_dict["description"] = 'Not Found'
    wiki_json = json.dumps(wiki_dict, ensure_ascii=False)
    return HttpResponse(wiki_json, content_type="application/json; charset=utf-8")


def show_wikis_by_keyword(request):
    _user = get_valid_user(request)
    if _user:
        _company=_user.company
        keyword=request.POST.get("s","")
        if keyword:
            _wikis=Wiki.objects.filter(Q(abbr__icontains=keyword) | Q(expression__icontains=keyword) | Q(description__icontains=keyword), company=_company)
        else:
            _wikis=Wiki.objects.filter(company=_company).order_by("-edit_time")[0:20]
        return render(request, 'wiki.html', {'current_user':_user, 'wikis':_wikis})
    return HttpResponseRedirect('/login')


def create_wiki(request):
    _user = get_valid_user(request)
    if _user:
        if request.method=="POST":
            _abbr=request.POST.get("abbr","")
            _expression=request.POST.get("expression","")
            _description=request.POST.get("description","")
            if _abbr or _expression:
                Wiki.objects.create(contributor=_user, abbr=_abbr, expression=_expression, description=_description, company=_user.company)
        return HttpResponseRedirect('/wiki')
    return HttpResponseRedirect('/login')
