# coding=utf-8
from django.shortcuts import render
from usermgmt.utils import get_valid_user
from django.contrib import messages
from django.http import HttpResponseRedirect
from pmp.cache import get_product_types_catalog, get_products_catalog_by_pseudo_name
from models import *


def show_all_catalog(request):
    _user=get_valid_user(request)
    product_types=get_product_types_catalog()
    return render(request, 'sec_eco.html',{'current_user':_user, 'product_types':product_types})


def show_catalog(request, product_type_pseudo):
    _user=get_valid_user(request)
    (product_type, products)=get_products_catalog_by_pseudo_name(product_type_pseudo)
    if not product_type:
        messages.add_message(request, messages.INFO, '参数错误!')
        return HttpResponseRedirect('/catalog')
    return render(request, 'sec_products.html',{'current_user':_user, 'product_type':product_type, 'products':products})
