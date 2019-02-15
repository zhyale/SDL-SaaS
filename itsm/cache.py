# coding=utf-8
from django.core.cache import cache
from models import *

# cache time by minutes * seconds
CACHE_TIMEOUT = 1 * 10


def get_ci_set(_user):
    cache_key='CI_SET_'+_user.company.top_domain_name
    ci_set=cache.get(cache_key)
    if not ci_set:
        ci_set={}
        cis=CI.objects.filter(company=_user.company).order_by('category','-create_time')[0:100]
        ci_set["cis"]=cis
        cache.set(cache_key, ci_set, CACHE_TIMEOUT)
    return ci_set

def get_all_ip(_user, clear_cache):
    cache_key='IP_SET_'+_user.company.top_domain_name
    if clear_cache:
        cache.delete(cache_key)
        ip_set=None
    else:
        ip_set=cache.get(cache_key)
    if not ip_set:
        ip_set=_user.company.company_ips.order_by('name')
        cache.set(cache_key, ip_set, CACHE_TIMEOUT)
    return ip_set


def get_all_domain(_user, clear_cache):
    cache_key='DOMAIN_SET_'+_user.company.top_domain_name
    if clear_cache:
        cache.delete(cache_key)
        domain_set=None
    else:
        domain_set=cache.get(cache_key)
    if not domain_set:
        domain_set=_user.company.company_domains.all()
        cache.set(cache_key, domain_set, CACHE_TIMEOUT)
    return domain_set
