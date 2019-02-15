# coding=utf-8
from django.core.cache import cache
from django.shortcuts import render
from flowmgmt.models import ProjectFlow, TaskFlow
from flowmgmt.utils import project_flow_json, task_flow_json
from taskmgmt.models import Task
from pagemgmt.models import Page
from ecomgmt.models import ProductType
from usermgmt.models import DayStat
from pmp.settings import BASE_DIR, SAAS_PORTAL,DEBUG
import os
import rsa
import datetime


# cache time by minutes * seconds
CACHE_TIMEOUT = 60 * 60
if DEBUG:
    CACHE_TIMEOUT=1


def get_guest_index_cache(request):
    response = cache.get('guest_index')
    if not response:
        _project_agl_flow = get_project_flow_by_type('AGL')
        # _project_app_flow = get_project_flow_by_type('APP')
        agl_flow_json = get_project_flow_json_by_id(_project_agl_flow.id)
        # app_flow_json = get_project_flow_json_by_id(_project_app_flow.id)
        _pages = get_front_pages()
        _carousel_pages=get_carousel_pages()
        response = render(request, 'index.html',
                          {'agl_flow_json': agl_flow_json, 'pages': _pages, 'carousel_pages': _carousel_pages})
        cache.set('guest_index', response, CACHE_TIMEOUT)
    return response


def get_project_flow_by_id(flow_id):
    flow_cache_key='PROJECT_FLOW_'+str(flow_id)
    _flow=cache.get(flow_cache_key)
    if not _flow:
        _flow=ProjectFlow.objects.get(id=flow_id)
        cache.set(flow_cache_key, _flow, CACHE_TIMEOUT)
    return _flow


def get_project_flow_json_by_id(flow_id):
    flow_cache_key='PROJECT_FLOW_JSON'+str(flow_id)
    flow_json=cache.get(flow_cache_key)
    if not flow_json:
        flow_json=project_flow_json(flow_id)
        cache.set(flow_cache_key, flow_json, CACHE_TIMEOUT)
    return flow_json


def get_project_flow_by_type(flow_type):
    flow_cache_key='PROJECT_FLOW_'+flow_type
    _flow=cache.get(flow_cache_key)
    if not _flow:
        _flow=ProjectFlow.objects.get(type=flow_type)
        cache.set(flow_cache_key, _flow, CACHE_TIMEOUT)
    return _flow


def get_front_pages():
    front_pages = cache.get('front_pages')
    if not front_pages:
        front_pages = Page.objects.filter(show_in_front=True).order_by('-time')
        cache.set('front_pages', front_pages, CACHE_TIMEOUT)
    return front_pages


def get_carousel_pages():
    carousel_pages = cache.get('carousel_pages')
    if not carousel_pages:
        carousel_pages = Page.objects.filter(show_in_carousel=True).order_by('-time')
        cache.set('carousel_pages', carousel_pages, CACHE_TIMEOUT)
    return carousel_pages


def get_page_by_pseudo_name(pseudo_link):
    page_cache_key = 'page_' + pseudo_link
    _page = cache.get(page_cache_key)
    if not _page:
        try:
            _page = Page.objects.get(pseudo_name=pseudo_link)
        except:
            _page=None
        cache.set(page_cache_key, _page, CACHE_TIMEOUT)
    return _page


def get_task_flow_by_type(flow_type):
    flow_cache_key='TASK_FLOW_'+flow_type
    _flow=cache.get(flow_cache_key)
    if not _flow:
        _flow=TaskFlow.objects.get(type=flow_type)
        cache.set(flow_cache_key, _flow, CACHE_TIMEOUT)
    return _flow


def get_task_flow_by_id(flow_id):
    flow_cache_key='TASK_FLOW_'+str(flow_id)
    _flow=cache.get(flow_cache_key)
    if not _flow:
        _flow=TaskFlow.objects.get(id=flow_id)
        cache.set(flow_cache_key, _flow, CACHE_TIMEOUT)
    return _flow


def get_task_flow_json_by_id(flow_id):
    flow_cache_key='TASK_FLOW_JSON'+str(flow_id)
    flow_json=cache.get(flow_cache_key)
    if not flow_json:
        flow_json=task_flow_json(flow_id)
        cache.set(flow_cache_key, flow_json, CACHE_TIMEOUT)
    return flow_json


def get_priv_key():
    privkey=cache.get('RSA_PRIV_KEY')
    if not privkey:
        privkey_file=os.path.join(BASE_DIR, 'privkey_1024.pem')
        with open(privkey_file) as pfile:
            pkcs1 = pfile.read()
            privkey = rsa.PrivateKey.load_pkcs1(pkcs1)
            cache.set('RSA_PRIV_KEY', privkey, CACHE_TIMEOUT)
    return privkey


def get_cache_value_by_key(key):
    return cache.get(key)


def clear_cache_by_key(key):
    value = cache.get(key)
    if value:
        cache.delete(key)
    return


def get_task_by_id(tid):
    if not tid:
        return None
    cache_key='TASK_INFO_'+str(tid)
    task=cache.get(cache_key)
    if not task:
        try:
            task=Task.objects.get(id=tid)
        except:
            task=None
        cache.set(cache_key, task, CACHE_TIMEOUT)
    return task


def clear_task_cache_by_id(tid):
    cache_key='TASK_INFO_'+str(tid)
    task=cache.get(cache_key)
    if task:
        cache.delete(cache_key)
    return


def get_product_types_catalog():
    cache_key='PRODUCT_TYPES_CATALOG'
    product_types=cache.get(cache_key)
    if not product_types:
        product_types=ProductType.objects.order_by('sort_no')
        cache.set(cache_key, product_types, CACHE_TIMEOUT)
    return product_types


def get_products_catalog_by_pseudo_name(product_type_pseudo):
    cache_key='PRODUCT_'+product_type_pseudo
    cache_value=cache.get(cache_key)
    if not cache_value:
        try:
            product_type=ProductType.objects.get(pseudo_name=product_type_pseudo)
            products=product_type.type_products.order_by('sort_no')
            cache_value=(product_type, products)
        except:
            cache_value = (None, None)
        cache.set(cache_key, cache_value, CACHE_TIMEOUT)
    return cache_value


def update_today_statistics(current_user):
    today=datetime.date.today()
    today_start=datetime.datetime(today.year, today.month, today.day)
    now=datetime.datetime.now()
    timeout=86400-int((now-today_start).total_seconds())
    cache_key="DAYSTAT_" + today.strftime("%Y%m%d")
    today_stat=cache.get(cache_key)
    if not today_stat:
        try:
            today_stat=DayStat.objects.get(date=today)
        except:
            today_stat=DayStat.objects.create(pv=0)
    today_stat.pv = today_stat.pv + 1
    if current_user:
        today_stat.visitors.add(current_user)
    cache.set(cache_key, today_stat, timeout)
    # save statistics to database every X minutes
    last_save_time=cache.get("STAT_LAST_SAVE_TIME")
    if not last_save_time:
        cache.set("STAT_LAST_SAVE_TIME", now, timeout)
        today_stat.save()
        return
    save_interval=int((now-last_save_time).total_seconds())
    if save_interval>60:
        today_stat.save()
        cache.set("STAT_LAST_SAVE_TIME", now, CACHE_TIMEOUT)
    return


def get_site_map():
    cache_key='SITEMAP'
    xml=cache.get(cache_key)
    if not xml:
        xml = '<?xml version="1.0" encoding="UTF-8"?>\r\n'
        xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\r\n'
        # Front page
        xml += '<url><loc>http://saas.janusec.com/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>'
        xml += '<url><loc>http://saas.janusec.com/itsm/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>'
        # Menu and fix urls
        fix_urls=['/signup','/login', '/kcp', '/term', '/faq', '/catalog', '/aboutus', '/password/generator', '/tools', '/tool/ip']
        for url in fix_urls:
            pagexml='<url>\r\n'
            pagexml += '<loc>'+ SAAS_PORTAL + url + '</loc>\r\n'
            pagexml += '<changefreq>weekly</changefreq>\r\n'
            pagexml += '<priority>0.9</priority>\r\n'
            pagexml += '</url>\r\n'
            xml += pagexml
        # catalog products
        product_types=ProductType.objects.all()
        for product_type in product_types:
            pagexml='<url>\r\n'
            pagexml += '<loc>'+ SAAS_PORTAL + '/catalog/'+ product_type.pseudo_name+ '</loc>\r\n'
            pagexml += '<changefreq>weekly</changefreq>\r\n'
            pagexml += '<priority>0.9</priority>\r\n'
            pagexml += '</url>\r\n'
            xml += pagexml
        # collect all pages
        pages=Page.objects.all()
        for page in pages:
            pagexml='<url>\r\n'
            pagexml += '<loc>'+ SAAS_PORTAL + '/content/'+ page.pseudo_name+ '</loc>\r\n'
            pagexml += '<changefreq>weekly</changefreq>\r\n'
            pagexml += '<priority>0.8</priority>\r\n'
            pagexml += '</url>\r\n'
            xml += pagexml
        # End tag
        xml += '</urlset>'
        cache.set(cache_key, xml, CACHE_TIMEOUT)
    return xml


def get_robots():
    cache_key='ROBOTS'
    robots=cache.get(cache_key)
    if not robots:
        robots='User-agent: *\r\n'
        robots += 'Disallow: /projectlist/\r\n'
        robots += 'Disallow: /tasklist/\r\n'
        robots += 'Disallow: /flowlist\r\n'
        robots += 'Disallow: /team\r\n'
        robots += 'Disallow: /wiki\r\n'
        robots += 'Disallow: /msglist\r\n'
        robots += 'Disallow: /circle\r\n'
        robots += 'Disallow: /specifications\r\n'
        robots += 'Disallow: /suggest\r\n'
        robots += '\r\n'
        robots += 'Sitemap: '+SAAS_PORTAL+'/sitemap.xml\r\n'
        cache.set(cache_key, robots, CACHE_TIMEOUT)
    return robots
